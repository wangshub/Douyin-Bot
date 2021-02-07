package com.humi.app.tripart.front.service;

import cn.hutool.core.date.DateField;
import cn.hutool.core.date.DateTime;
import cn.hutool.core.date.DateUtil;
import cn.hutool.core.date.TimeInterval;
import cn.hutool.core.util.RandomUtil;
import com.alibaba.fastjson.TypeReference;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.core.toolkit.IdWorker;
import com.google.common.collect.Maps;
import com.humi.app.tripart.common.bean.IotCommonResponse;
import com.humi.app.tripart.common.dao.HmIotEquipmentLogMapper;
import com.humi.app.tripart.common.dao.HmIotEquipmentMapper;
import com.humi.app.tripart.common.dao.HmIotEquipmentParameterMapper;
import com.humi.app.tripart.common.dict.IotData;
import com.humi.app.tripart.common.entity.HmIotEquipmentEntity;
import com.humi.app.tripart.common.entity.HmIotEquipmentLogEntity;
import com.humi.app.tripart.common.entity.HmIotEquipmentParameterEntity;
import com.humi.app.tripart.common.service.HmIotEquipmentService;
import com.humi.app.tripart.common.util.CommonUtil;
import com.humi.app.tripart.common.util.HMAC_SHA1;
import com.humi.app.tripart.common.util.OkHttpUtil;
import com.humi.app.tripart.front.dao.FrontHmIotEquipmentLogMapper;
import com.humi.app.tripart.front.dao.FrontHmIotEquipmentMapper;
import com.humi.app.tripart.front.model.enu.CardStatisticalEnum;
import com.humi.app.tripart.front.model.enu.ChartStatisticalEnum;
import com.humi.app.tripart.front.model.equipment.*;
import com.humi.app.tripart.manager.dao.ManagerEquipmentLogMapper;
import com.humi.app.tripart.manager.model.ManagerEquipmentHmIotInfoJsonRequest;
import com.humi.app.tripart.manager.model.equipmentlog.EquipmentContextLogResponseBean;
import com.humi.app.tripart.manager.service.ManagerEquipmentService;
import com.humi.app.tripart.manager.service.ManagerIotEquipmentLogService;
import com.humi.cloud.common.exception.HumiRuntimeException;
import com.humi.cloud.common.model.ResponseCode;
import com.humi.cloud.common.model.Result;
import com.humi.cloud.common.utils.ObjectUtil;
import com.humi.cloud.common.utils.crypt.BASE64Util;
import com.humi.cloud.mybatis.support.model.Page;
import com.humi.cloud.redis.helper.RedisCacheHelper;
import com.humi.cloud.security.support.utils.SecurityUtil;
import lombok.Synchronized;
import lombok.extern.slf4j.Slf4j;
import net.sf.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.text.DecimalFormat;
import java.util.*;

/**
 * 
 * <pre>
 * <b>Description: 前台设备</b>
 * <b>Author: autoCode v1.0</b>
 * <b>Date: 2020-07-21</b>
 * </pre>
 */
@Slf4j
@Service
public class FrontIotEquipmentService {

	//设备逻辑处理层
	@Autowired
	ManagerEquipmentService managerEquipmentService;

	// 设备service
	@Autowired
	HmIotEquipmentService baseService;

	@Autowired
	HmIotEquipmentMapper customMapper;

	@Autowired
	FrontHmIotEquipmentMapper frontHmIotEquipmentMapper;

	@Autowired
	HmIotEquipmentParameterMapper hmIotEquipmentParameterMapper;

	@Autowired
	FrontHmIotEquipmentLogMapper frontHmIotEquipmentLogMapper;

	@Autowired
	ManagerIotEquipmentLogService managerIotEquipmentLogService;

	@Autowired
	private HmIotEquipmentLogMapper hmIotEquipmentLogMapper;

	@Autowired
	private ManagerEquipmentLogMapper managerEquipmentLogMapper;

	@Value("${iot.demonstrate.user.id}")
	private String demonstrateUserId;

	/**
	 *
	 * <pre>
	 * 前台设备数量查询
	 * </pre>
	 *
	 * @return
	 */
	@Transactional
	public Result queryEquipmentCountBak(FrontIotEquipmentListCityRequest query) {
		//设备状态 0 离线 1在线 3 未激活
		Integer connectCount=0;
		Integer lostCount= 0;
		Integer onlineCount=0;
		Integer faultRate=0;
		/*List<HmIotEquipmentEntity> list = baseService.list(new LambdaQueryWrapper<HmIotEquipmentEntity>()
				.eq(HmIotEquipmentEntity::getUserId, SecurityUtil.getUser().getSourceId()));*/

		Page<FrontIotEquipmentListCityResponse, FrontIotEquipmentListCityRequest> page = new Page<>(query.getCurrent(), query.getSize(), query);
		customMapper.getIotEquipmentMain(page);
		List<FrontIotEquipmentListCityResponse> list = page.getRecords();
		ManagerEquipmentHmIotInfoJsonRequest info=null;
		for(int i=0;i<list.size();i++){
			 info = managerEquipmentService.queryEquipmentInfoByList(list.get(i).getDeviceNameUuid(),list.get(i).getProductId());
			if(info.getOnline()!=list.get(i).getState()){
				list.get(i).setState(info.getOnline());
			}
			if(info.getOnline()==0){
				lostCount +=1;
			}
			if(info.getOnline()==1){
				onlineCount +=1;
			}
		}
		FrontIotEquipmentCountResponse dest=new FrontIotEquipmentCountResponse();
		connectCount=onlineCount+lostCount;
		dest.setConnectCount(connectCount);
		dest.setLostCount(lostCount);
		dest.setOnlineCount(onlineCount);
		//故障率
		float num = (float)lostCount / connectCount;
		DecimalFormat df = new DecimalFormat("0.00");

		dest.setFaultRate(df.format(num));
		return Result.ok("查询成功",dest);
	}

	public Result queryEquipmentCount(FrontIotEquipmentListCityRequest query) {
		// 双跨之用 begin
		// 演示账号id与当前登录账号id相等，则查询所有设备数量
		if(ObjectUtil.isNotEmpty(demonstrateUserId) && demonstrateUserId.equals(query.getUserId())){
			query.setUserId(null);
		}
		// 双跨之用 end
		TimeInterval timer = DateUtil.timer();
		FrontIotEquipmentCountResponse dest = customMapper.getEquipmentCount(query);
		log.info("调用humi-app-tripart/front/equipment/queryEquipmentCount接口，查询数据库耗时：{}", DateUtil.formatBetween(timer.intervalRestart()));
		Integer connectCount = dest.getOnlineCount() + dest.getLostCount();
		dest.setConnectCount(connectCount);
		if(ObjectUtil.isNotEmpty(connectCount) && connectCount.intValue() > 0){
			//故障率
			float num = (float) dest.getLostCount() / (float) connectCount;
			DecimalFormat df = new DecimalFormat("0.00");

			dest.setFaultRate(df.format(num));
		}else{
			dest.setFaultRate("0");
		}
		return Result.ok("查询成功",dest);
	}



	/**
	 *
	 * <pre>
	 * 根据地区查询设备集合
	 * </pre>
	 *
	 * @return
	 */
	@Transactional
	public Result queryEquipmentListByCityBak(FrontIotEquipmentListCityRequest query) {
		List<FrontIotEquipmentListCityResponse> list1=new ArrayList<>();
		/*List<HmIotEquipmentEntity> list = baseService.list(new LambdaQueryWrapper<HmIotEquipmentEntity>()
				.eq(HmIotEquipmentEntity::getUserId, SecurityUtil.getUser().getSourceId())
				.eq(HmIotEquipmentEntity::getProvinceName, query.getProvinceName()));*/
		Page<FrontIotEquipmentListCityResponse, FrontIotEquipmentListCityRequest> page = new Page<>(query.getCurrent(), query.getSize(), query);
		customMapper.getIotEquipmentMain(page);
		List<FrontIotEquipmentListCityResponse> list = page.getRecords();
		ManagerEquipmentHmIotInfoJsonRequest info = null;
		for(int i=0;i<list.size();i++){
			 info = managerEquipmentService.queryEquipmentInfoByList(list.get(i).getDeviceNameUuid(),list.get(i).getProductId());
			if(info.getOnline()!=list.get(i).getState()){
				list.get(i).setState(info.getOnline());
			}
			if(info.getOnline()!=3){
				list1.add(list.get(i));
			}
		}
		return Result.ok("查询成功",list1);
	}

	public Result queryEquipmentListByCity(FrontIotEquipmentListCityRequest query) {
		// 双跨之用 begin
		// 演示账号id与当前登录账号id相等，则查询所有设备列表
		if(ObjectUtil.isNotEmpty(demonstrateUserId) && demonstrateUserId.equals(query.getUserId())){
			query.setUserId(null);
		}
		// 双跨之用 end
		TimeInterval timer = DateUtil.timer();
		List<FrontIotEquipmentListCityResponse> list1 = new ArrayList<>();
		Page<FrontIotEquipmentListCityResponse, FrontIotEquipmentListCityRequest> page = new Page<>(query.getCurrent(), query.getSize(), query);
		customMapper.getIotEquipmentMain(page);
		log.info("调用humi-app-tripart/front/equipment/queryEquipmentListByCity接口，查询数据库耗时：{}", DateUtil.formatBetween(timer.intervalRestart()));
		List<FrontIotEquipmentListCityResponse> list = page.getRecords();
		FrontIotEquipmentListCityResponse info = null;
		for(int i=0;i<list.size();i++){
			info = list.get(i);
			if(info.getState().intValue()!=3){
				list1.add(list.get(i));
			}
		}
		return Result.ok("查询成功",list1);
	}

	/**
	 * <pre>
	 * 查询设备详情
	 * </pre>
	 * @return
	 */
	@Transactional
	public Result queryEquipmentInfo(FrontIotEquipmentInfoRequest query) {
		HmIotEquipmentEntity old = baseService.getOne(new LambdaQueryWrapper<HmIotEquipmentEntity>()
				.eq(HmIotEquipmentEntity::getUserId, SecurityUtil.getUser().getSourceId())
				.eq(HmIotEquipmentEntity::getDeviceNameUuid, query.getDeviceNameUuid()));
		ManagerEquipmentHmIotInfoJsonRequest dest = managerEquipmentService.queryEquipmentInfoByList(query.getDeviceNameUuid(), old.getProductId());
		old.setState(dest.getOnline());
		return Result.ok("查询成功",old);
	}

	@Scheduled(cron="${equipment.random.offline.time}")
	@Synchronized
	public void randomUpdateEquipmentOffline(){
		new Thread(() -> {
			TimeInterval timer = DateUtil.timer();
			// 定时获取近一周设备数量，并存入redis
			Integer equipmentWeekCount = baseService.count(new LambdaQueryWrapper<HmIotEquipmentEntity>().between(HmIotEquipmentEntity::getCreateTime, com.humi.cloud.common.utils.DateUtil.getDate(com.humi.cloud.common.utils.DateUtil.getLaterDayDate(-7)), com.humi.cloud.common.utils.DateUtil.getDate("yyyy-MM-d")));
			RedisCacheHelper.setValue(CommonUtil.IOT_EQUIPMENT_WEEK_COUNT_KEY, equipmentWeekCount);
			log.info("定时任务，查询近一周设备数量并存入Redis缓存，耗时：{}", DateUtil.formatBetween(timer.intervalRestart()));
			// 定时随机离线1%~10%数量的设备
			Integer totalCount = baseService.count();
			if(ObjectUtil.isNotEmpty(totalCount) && totalCount.intValue() > 0){
				baseService.update(new UpdateWrapper<HmIotEquipmentEntity>().lambda().set(HmIotEquipmentEntity::getState, 1).eq(HmIotEquipmentEntity::getState, 0));
				frontHmIotEquipmentMapper.randomUpdateEquipmentOffline(totalCount*RandomUtil.randomInt(1, 10)/100);
			}
			log.info("定时任务，随机离线1%~10%数量的设备，耗时：{}", DateUtil.formatBetween(timer.intervalRestart()));
		}).start();
	}

	/**
	 * 获取统计数据
	 */
	public Result getStatisticalData(){
		Map<String,Object> response = new HashMap<>();
		response.put("equipmentCount",baseService.count());
		response.put("equipmentCoverageArea",customMapper.getProvinceName());
		response.put("deviceConnection",customMapper.getEquipmentDetails());
		return Result.ok(response);
	}
	public Integer getStatisticalCardData(String cardCode){
		if(CardStatisticalEnum.connectingDevices.getCode().equals(cardCode)){
			return baseService.count();
		}
		if(CardStatisticalEnum.connectingDevicesRegion.getCode().equals(cardCode)){
			return customMapper.getProvinceName();
		}
		return 0;
	}
	public Object getStatisticalChartData(String cardCode){
		if(ChartStatisticalEnum.devicesMaps.getCode().equals(cardCode)){
			return customMapper.getEquipmentDistributionArea();
		}
		if(ChartStatisticalEnum.connectingDevicesType.getCode().equals(cardCode)){
			return customMapper.getEquipmentDetails();
		}
		return null;
	}
	/**
	 * 获取设备分布地区
	 */
	public Result getEquipmentDistributionArea(){
		return Result.ok(customMapper.getEquipmentDistributionArea());
	}

	public Result getEquipmentParameterList(String equipmentId){
		HmIotEquipmentEntity equipmentEntity = baseService.getById(equipmentId);
		if(ObjectUtil.isEmpty(equipmentEntity)){
			log.error("此设备不存在！设备id【{}】", equipmentId);
			throw HumiRuntimeException.newInstance(ResponseCode.FAILED, "此设备不存在！");
		}
		if(ObjectUtil.isNotEmpty(equipmentEntity.getDataFlag()) && equipmentEntity.getDataFlag().intValue() == 1) {
			batchGenerationContextLogByProductIdWithFrequency(equipmentEntity, 100);
		}else{
			batchPullTencentIotEquipmentLog(equipmentEntity);
		}
		HmIotEquipmentLogEntity logEntity = frontHmIotEquipmentLogMapper.getCurrentEquipmentLog(equipmentEntity.getDeviceNameUuid());
		JSONObject jsonObject = null;
		try {
			if (ObjectUtil.isNotEmpty(logEntity) && ObjectUtil.isNotEmpty(logEntity.getPayload())) {
				String payload = BASE64Util.decrypt(logEntity.getPayload().replace("}", ""));
				if(ObjectUtil.isNotEmpty(payload)){
					jsonObject = JSONObject.fromObject(payload);
				}
				log.info("解析设备【{}】，关键字【{}】，日志内容【{}】",equipmentEntity.getDeviceName(), equipmentEntity.getTempletId(), payload);
			}
		}catch(Exception ex){
			log.error("解析设备【{}】，关键字【{}】，内容日志【{}】，异常：{}",equipmentEntity.getDeviceName(), equipmentEntity.getTempletId(), logEntity.getPayload(), ex);
		}
		List<HmIotEquipmentParameterEntity> parameterEntityList = hmIotEquipmentParameterMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentParameterEntity>().eq(HmIotEquipmentParameterEntity::getTempletId, equipmentEntity.getTempletId()));
		List<FrontIotEquipmentParameterResponse> parameterResponseList = null;
		if(ObjectUtil.isNotEmpty(parameterEntityList) && parameterEntityList.size() > 0){
			parameterResponseList = new ArrayList<>();
			FrontIotEquipmentParameterResponse parameterResponse = null;
			for(HmIotEquipmentParameterEntity parameterEntity: parameterEntityList){
				parameterResponse = new FrontIotEquipmentParameterResponse();
				parameterResponse.setParameterName(parameterEntity.getParameterName());
				parameterResponse.setParameterCode(parameterEntity.getParameterCode());
				if(ObjectUtil.isNotEmpty(logEntity) && ObjectUtil.isNotEmpty(logEntity.getDateTime())) {
					parameterResponse.setParameterDate(logEntity.getDateTime());
				}
				try {
					if (ObjectUtil.isNotEmpty(jsonObject)) {
						String parameterValue = jsonObject.getString(parameterEntity.getParameterCode());
						parameterResponse.setParameterValue(parameterValue);
					}
				}catch(Exception ex){
					log.error("获取JSONObject对象属性异常：{}", ex);
				}
				parameterResponseList.add(parameterResponse);
			}
		}
		return Result.ok(parameterResponseList);
	}

	public Result getEquipmentContentLogList(FrontIotEquipmentContentLogRequest request){
		HmIotEquipmentEntity equipmentEntity = baseService.getById(request.getEquipmentId());
		Map<String, Object> map = Maps.newHashMap();
		if(ObjectUtil.isNotEmpty(equipmentEntity)){
			List<HmIotEquipmentParameterEntity> parameterEntityList = hmIotEquipmentParameterMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentParameterEntity>().eq(HmIotEquipmentParameterEntity::getTempletId, equipmentEntity.getTempletId()));
			if(ObjectUtil.isNotEmpty(parameterEntityList) && parameterEntityList.size() > 0) {
				List<FrontIotEquipmentContentLogResponse> logEntityList = frontHmIotEquipmentLogMapper.getEquipmentContentLogList(equipmentEntity.getProductId(), equipmentEntity.getDeviceNameUuid(), request.getSize());
				List<Map<String, Object>> paramterLogList = null;
				for(HmIotEquipmentParameterEntity parameterEntity: parameterEntityList){
					if(ObjectUtil.isNotEmpty(logEntityList) && logEntityList.size() > 0){
						paramterLogList = new ArrayList<>();
						Map<String, Object> paramLogMap = null;
						for(FrontIotEquipmentContentLogResponse response: logEntityList){
							paramLogMap = new HashMap<String, Object>();
							try {
								JSONObject jsonObject = JSONObject.fromObject(response.getPayload());
								paramLogMap.put("parameterName", parameterEntity.getParameterName());
								paramLogMap.put("parameterCode", parameterEntity.getParameterCode());
								paramLogMap.put("parameterValue", jsonObject.get(parameterEntity.getParameterCode()));
								paramLogMap.put("dateTime", response.getDateTime());
								paramterLogList.add(paramLogMap);
							}catch(Exception ex){
								log.error("解析设备内容日志异常：{}", ex);
							}
						}
						map.put(parameterEntity.getParameterCode(), paramterLogList);
					}
				}
			}
		}
		return Result.ok(map);
	}

	private void batchGenerationContextLogByProductIdWithFrequency(HmIotEquipmentEntity equipmentEntity, Integer size){
		TimeInterval timer = cn.hutool.core.date.DateUtil.timer();
		DateTime endDateTime = DateUtil.date();
		Calendar endCalendar = endDateTime.toCalendar(TimeZone.getTimeZone("GMT+08:00"));
		DateTime beginDateTime = null;
		if(ObjectUtil.isNotEmpty(equipmentEntity.getFrequency())){
			endCalendar.set(Calendar.MILLISECOND, 0);
			if(equipmentEntity.getFrequency().equals("10s")){
				endCalendar.set(Calendar.SECOND, CommonUtil.getTotalTen(endDateTime.getSeconds()));
				beginDateTime = DateUtil.offset(endCalendar.getTime(), DateField.SECOND, -(size*10));
			}else if(equipmentEntity.getFrequency().equals("1m")){
				endCalendar.set(Calendar.SECOND, 0);
				beginDateTime = DateUtil.offset(endCalendar.getTime(), DateField.MINUTE, -(size*1));
			}else if(equipmentEntity.getFrequency().equals("10m")){
				endCalendar.set(Calendar.MINUTE, CommonUtil.getTotalTen(endDateTime.getMinutes()));
				endCalendar.set(Calendar.SECOND, 0);
				beginDateTime = DateUtil.offset(endCalendar.getTime(), DateField.MINUTE, -(size*10));
			}else if(equipmentEntity.getFrequency().equals("30m")){
				endCalendar.set(Calendar.MINUTE, CommonUtil.getTotalThirty(endDateTime.getMinutes()));
				endCalendar.set(Calendar.SECOND, 0);
				beginDateTime = DateUtil.offset(endCalendar.getTime(), DateField.MINUTE, -(size*30));
			}else if(equipmentEntity.getFrequency().equals("60m")){
				endCalendar.set(Calendar.MINUTE, 0);
				endCalendar.set(Calendar.SECOND, 0);
				beginDateTime = DateUtil.offset(endCalendar.getTime(), DateField.HOUR_OF_DAY, -(size*1));
			}
		}
		if(ObjectUtil.isNotEmpty(beginDateTime)) {
			String endDateTimeStr = DateUtil.format(endCalendar.getTime(), "yyyy-MM-dd HH:mm:ss");
			String beginDateTimeStr = DateUtil.format(beginDateTime.toJdkDate(), "yyyy-MM-dd HH:mm:ss");
			managerIotEquipmentLogService.batchGenerationContextLogByProductIdWithFrequency(equipmentEntity, beginDateTimeStr, endDateTimeStr, size);
			log.info("调用humi-app-tripart/front/equipment/getEquipmentContentLogList接口，根据规则批量生成设备【{}】【{}~{}】【{}】的内容日志，耗时【{}】", equipmentEntity.getDeviceName(), beginDateTimeStr, endDateTimeStr, equipmentEntity.getFrequency(), cn.hutool.core.date.DateUtil.formatBetween(timer.intervalRestart()));
		}
	}

	private void batchPullTencentIotEquipmentLog(HmIotEquipmentEntity equipmentEntity){
		try {
			String productId = equipmentEntity.getProductId();
			String strEnd = "";
			int timeStamp = (int) (System.currentTimeMillis() / 1000);
			UUID uuid = UUID.randomUUID();//Nonce uuid随机生成
			String postName = IotData.DATAPOST.getName();//post请求头

			Map<String, Object> map = new LinkedHashMap<>();
			map.put("Action", "ListLogPayload");
//		if(!"".equals(query.getContext()) && query.getContext()!=null){
//			map.put("Context", query.getContext());
//		}
//		if(!"".equals(query.getKeywords()) && query.getKeywords()!=null){
			map.put("Keywords", "productid:" + productId);
//		}
//		if(!"".equals(query.getMaxNum()) && query.getMaxNum()!=null&&query.getMaxNum()!=0){
			map.put("MaxNum", 50);
//		}
			DateTime currentDateTime = DateUtil.date();
			DateTime beforeDateTime = DateUtil.offset(currentDateTime.toJdkDate(), DateField.DAY_OF_YEAR, -7);
			Long maxTime = DateUtil.current(false);
			Long minTime = beforeDateTime.getTime();
			map.put("MaxTime", maxTime);
			map.put("MinTime", minTime);
			map.put("Nonce", uuid);
			map.put("Region", IotData.REGION.getName());
			map.put("SecretId", IotData.SECRETID.getName());
			map.put("Timestamp", timeStamp);
			map.put("Version", IotData.VERSION.getName());
			for (Map.Entry<String, Object> entry : map.entrySet()) {
				String mapKey = entry.getKey();
				Object mapValue = entry.getValue();
				strEnd += mapKey + "=" + mapValue + "&";
			}
			String str = strEnd.substring(0, strEnd.length() - 1);
			System.out.println(str);
			String signature = HMAC_SHA1.genHMAC(postName + str, IotData.SECRETKEY.getName());
			System.out.println(signature);
			System.out.println(postName + str);
			map.put("Signature", signature);
			String result = OkHttpUtil.postFormBody1(IotData.HTTP.getName(), map);
			IotCommonResponse<EquipmentContextLogResponseBean> contextLog = com.alibaba.fastjson.JSONObject.parseObject(result, new TypeReference<IotCommonResponse<EquipmentContextLogResponseBean>>() {
			});
			if (ObjectUtil.isNotEmpty(contextLog)
					&& ObjectUtil.isNotEmpty(contextLog.getResponse().getResults())
					&& contextLog.getResponse().getResults().size() > 0) {
				List<HmIotEquipmentLogEntity> logEntityList = new ArrayList<>();
				HmIotEquipmentLogEntity entity = null;
				for (EquipmentContextLogResponseBean bean : contextLog.getResponse().getResults()) {
					List<HmIotEquipmentLogEntity> existsList = hmIotEquipmentLogMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentLogEntity>().eq(HmIotEquipmentLogEntity::getProductId, productId).eq(HmIotEquipmentLogEntity::getDateTime, com.humi.cloud.common.utils.DateUtil.format("yyyy-MM-dd HH:mm:ss", Long.valueOf(bean.getDateTime()))));
					if (ObjectUtil.isEmpty(existsList) || existsList.size() <= 0) {
						entity = new HmIotEquipmentLogEntity();
						//设备日志类型 1-行为日志 2-内容日志 3-设备日志
						entity.setId(IdWorker.getIdStr());
						entity.setType("2");
						entity.setProductId(productId);
						entity.setDeviceName(bean.getDeviceName());
						entity.setRequestId(bean.getRequestID());
						entity.setSrcName(bean.getSrcName());
						entity.setTopic(bean.getTopic());
						entity.setPayload(bean.getPayload());
						entity.setPayloadFmtType(bean.getPayloadFmtType());
						entity.setDateTime(com.humi.cloud.common.utils.DateUtil.format("yyyy-MM-dd HH:mm:ss", Long.valueOf(bean.getDateTime())));
						entity.setUin(bean.getUin());
						entity.setCreateBy(SecurityUtil.getUser().getSourceId());
						entity.setUpdateBy(SecurityUtil.getUser().getSourceId());
						logEntityList.add(entity);
					}
				}
				if(ObjectUtil.isNotEmpty(logEntityList) && logEntityList.size() > 0) {
					managerEquipmentLogMapper.batchSave(logEntityList);
				}
			}
		}catch(Exception ex){
			log.error("从腾讯物联网平台拉取设备日志异常：{}", ex);
		}
	}

	public static void main(String[] args) {
//		DateTime currentDateTime = DateUtil.date();
//		DateTime beforeDateTime = DateUtil.offset(currentDateTime.toJdkDate(), DateField.DAY_OF_YEAR, -7);
//		Long maxTime = DateUtil.current(false);
//		Long minTime = beforeDateTime.getTime();
//		System.out.println(maxTime);
//		System.out.println(minTime);

		for(int i = 0;i < 173; i++){
			System.out.println(IdWorker.getIdStr());
		}
	}
}