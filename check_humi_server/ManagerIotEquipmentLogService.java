package com.humi.app.tripart.manager.service;

import cn.hutool.core.codec.Base64;
import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.date.DateField;
import cn.hutool.core.date.DateRange;
import cn.hutool.core.date.DateTime;
import cn.hutool.core.date.TimeInterval;
import cn.hutool.core.util.RandomUtil;
import com.alibaba.fastjson.JSON;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.IdWorker;
import com.google.common.collect.Maps;
import com.humi.app.tripart.common.bean.IotCommonResponse;
import com.humi.app.tripart.common.dao.HmIotEquipmentLogMapper;
import com.humi.app.tripart.common.dao.HmIotEquipmentMapper;
import com.humi.app.tripart.common.dao.HmIotEquipmentParameterMapper;
import com.humi.app.tripart.common.entity.HmIotEquipmentEntity;
import com.humi.app.tripart.common.entity.HmIotEquipmentLogEntity;
import com.humi.app.tripart.common.entity.HmIotEquipmentParameterEntity;
import com.humi.app.tripart.common.util.CommonUtil;
import com.humi.app.tripart.manager.dao.ManagerEquipmentLogMapper;
import com.humi.app.tripart.manager.model.ManagerEquipmentBehaviorLogRequest;
import com.humi.app.tripart.manager.model.ManagerEquipmentContextLogRequest;
import com.humi.app.tripart.manager.model.equipmentlog.EquipmentBehaviorLogResponseBean;
import com.humi.app.tripart.manager.model.equipmentlog.EquipmentContextLogResponseBean;
import com.humi.app.tripart.manager.model.equipmentlog.SearchEquipmentLogRequestBean;
import com.humi.cloud.common.utils.DateUtil;
import com.humi.cloud.common.utils.ObjectUtil;
import com.humi.cloud.mybatis.support.model.Page;
import com.humi.cloud.redis.helper.RedisCacheHelper;
import com.humi.cloud.security.support.utils.SecurityUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * <pre>
 * <b>Description: coding_team</b>
 * <b>@Author: autoCode v1.0</b>
 * <b>Date: 2020-11-09</b>
 * </pre>
 */
@Slf4j
@Service
public class ManagerIotEquipmentLogService {

	@Autowired
	private HmIotEquipmentLogMapper hmIotEquipmentLogMapper;

	@Autowired
	private ManagerEquipmentLogMapper managerEquipmentLogMapper;

	@Autowired
	private HmIotEquipmentMapper hmIotEquipmentMapper;

	@Autowired
	private HmIotEquipmentParameterMapper hmIotEquipmentParameterMapper;

	public IotCommonResponse<EquipmentBehaviorLogResponseBean> batchSaveBehaviorLog(ManagerEquipmentBehaviorLogRequest request, IotCommonResponse<EquipmentBehaviorLogResponseBean> behaviorLog){
		String productId = request.getKeywords().split(":")[1];
		if(ObjectUtil.isNotEmpty(behaviorLog)
				&& ObjectUtil.isNotEmpty(behaviorLog.getResponse().getResults())
				&& behaviorLog.getResponse().getResults().size() > 0
				&& ObjectUtil.isNotEmpty(request)
				&& ObjectUtil.isNotEmpty(request.getKeywords())) {
			HmIotEquipmentLogEntity entity = null;
			for(EquipmentBehaviorLogResponseBean bean: behaviorLog.getResponse().getResults()) {
				List<HmIotEquipmentLogEntity> existsList = hmIotEquipmentLogMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentLogEntity>().eq(HmIotEquipmentLogEntity::getProductId, productId).eq(HmIotEquipmentLogEntity::getTime, CommonUtil.UTCtoCST(bean.getTime(),"yyyy-MM-dd HH:mm:ss")));
				if(ObjectUtil.isEmpty(existsList) || existsList.size() <= 0) {
					entity = new HmIotEquipmentLogEntity();
					//设备日志类型 1-行为日志 2-内容日志 3-设备日志
					entity.setType("1");
					entity.setProductId(productId);
					entity.setContent(bean.getContent());
					entity.setResult(bean.getResult());
					entity.setScene(bean.getScene());
					entity.setTime(CommonUtil.UTCtoCST(bean.getTime(), "yyyy-MM-dd HH:mm:ss"));
					entity.setUserid(bean.getUserid());
					entity.setCreateBy(SecurityUtil.getUser().getSourceId());
					entity.setUpdateBy(SecurityUtil.getUser().getSourceId());
					hmIotEquipmentLogMapper.insert(entity);
				}
			}
		}
		String beginDateTime = DateUtil.getDatetime(Long.valueOf(request.getMinTime()));
		String endDateTime = DateUtil.getDatetime(Long.valueOf(request.getMaxTime()));
		batchGenerationBehaviorLogByProductId(productId, beginDateTime, endDateTime, request.getSize());
		SearchEquipmentLogRequestBean requestBean = new SearchEquipmentLogRequestBean();
		requestBean.setProductId(productId);
		requestBean.setMaxNum(request.getMaxNum());
		requestBean.setMinTime(beginDateTime);
		requestBean.setMaxTime(endDateTime);
		requestBean.setCurrent(request.getCurrent());
		requestBean.setSize(request.getSize());
		Page<EquipmentBehaviorLogResponseBean, SearchEquipmentLogRequestBean> page = new Page(requestBean.getCurrent(), requestBean.getSize(), requestBean);
		List<EquipmentBehaviorLogResponseBean> behaviorLogList = managerEquipmentLogMapper.searchEquipmentBehaviorLogPage(page);
		behaviorLog.getResponse().setResults(behaviorLogList);
		behaviorLog.getResponse().setTotalCount(behaviorLogList.size());
		return behaviorLog;
	}

	public IotCommonResponse<EquipmentContextLogResponseBean> batchSaveContextLog(ManagerEquipmentContextLogRequest query, IotCommonResponse<EquipmentContextLogResponseBean> contextLog){
		String productId = query.getKeywords().split(":")[1];
		if(ObjectUtil.isNotEmpty(contextLog)
				&& ObjectUtil.isNotEmpty(contextLog.getResponse().getResults())
				&& contextLog.getResponse().getResults().size() > 0) {
			HmIotEquipmentLogEntity entity = null;
			for(EquipmentContextLogResponseBean bean: contextLog.getResponse().getResults()) {
				List<HmIotEquipmentLogEntity> existsList = hmIotEquipmentLogMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentLogEntity>().eq(HmIotEquipmentLogEntity::getProductId, productId).eq(HmIotEquipmentLogEntity::getDateTime, DateUtil.format("yyyy-MM-dd HH:mm:ss", Long.valueOf(bean.getDateTime()))));
				if(ObjectUtil.isEmpty(existsList) || existsList.size() <= 0) {
					entity = new HmIotEquipmentLogEntity();
					//设备日志类型 1-行为日志 2-内容日志 3-设备日志
					entity.setType("2");
					entity.setProductId(productId);
					entity.setDeviceName(bean.getDeviceName());
					entity.setRequestId(bean.getRequestID());
					entity.setSrcName(bean.getSrcName());
					entity.setTopic(bean.getTopic());
					entity.setPayload(bean.getPayload());
					entity.setPayloadFmtType(bean.getPayloadFmtType());
					entity.setDateTime(DateUtil.format("yyyy-MM-dd HH:mm:ss", Long.valueOf(bean.getDateTime())));
					entity.setUin(bean.getUin());
					entity.setCreateBy(SecurityUtil.getUser().getSourceId());
					entity.setUpdateBy(SecurityUtil.getUser().getSourceId());
					hmIotEquipmentLogMapper.insert(entity);
				}
			}
		}
		String beginDateTime = null;
		String endDateTime = null;
		if(Long.valueOf(query.getMaxTime()) > Long.valueOf(query.getMinTime())){
			long current = cn.hutool.core.date.DateUtil.current(false);
			if(Long.valueOf(query.getMaxTime()) > current){
				query.setMaxTime(String.valueOf(current));
			}
			beginDateTime = DateUtil.getDatetime(Long.valueOf(query.getMinTime()));
			endDateTime = DateUtil.getDatetime(Long.valueOf(query.getMaxTime()));
			batchGenerationContextLogByProductId(productId, beginDateTime, endDateTime, query.getCurrent(), query.getSize());
		}
		SearchEquipmentLogRequestBean requestBean = new SearchEquipmentLogRequestBean();
		requestBean.setProductId(productId);
		requestBean.setMaxNum(query.getMaxNum());
		requestBean.setMinTime(beginDateTime);
		requestBean.setMaxTime(endDateTime);
		requestBean.setCurrent(query.getCurrent());
		requestBean.setSize(query.getSize());
		Page<EquipmentContextLogResponseBean, SearchEquipmentLogRequestBean> page = new Page(requestBean.getCurrent(), requestBean.getSize(), requestBean);
		List<EquipmentContextLogResponseBean> contextLogList = managerEquipmentLogMapper.searchEquipmentContextLogPage(page);
		contextLog.getResponse().setResults(contextLogList);
		contextLog.getResponse().setTotalCount(contextLogList.size());
		return contextLog;
	}

	private void batchGenerationBehaviorLogByProductId(String productId, String beginTime, String endTime, int size){
		List<DateTime> dateList = cn.hutool.core.date.DateUtil.rangeToList(DateUtil.parseDatetime(beginTime), DateUtil.parseDatetime(endTime), DateField.DAY_OF_YEAR);
		List<HmIotEquipmentEntity> equipmentEntityList = hmIotEquipmentMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentEntity>()
				.eq(HmIotEquipmentEntity::getProductId, productId)
				.in(HmIotEquipmentEntity::getWorkTime, "9-18", "9-20"));
		if(ObjectUtil.isNotEmpty(equipmentEntityList) && equipmentEntityList.size() > 0){
			HmIotEquipmentLogEntity logEntity = null;
			int count = 0;
			for(HmIotEquipmentEntity entity: equipmentEntityList){
				// 只有导入的设备数据才根据规则生成日志，双跨之用
				if(ObjectUtil.isNotEmpty(entity.getDataFlag()) && entity.getDataFlag().intValue() == 1) {
					int beginHourOfDay = Integer.valueOf(entity.getWorkTime().split("-")[0]).intValue();
					int endHourOfDay = Integer.valueOf(entity.getWorkTime().split("-")[1]).intValue();
					if (ObjectUtil.isNotEmpty(dateList) && dateList.size() > 0) {
						for (DateTime dateTime : dateList) {

							Calendar beginCalendar = dateTime.toCalendar(TimeZone.getTimeZone("GMT+08:00"));
							beginCalendar.set(Calendar.HOUR_OF_DAY, beginHourOfDay);
							beginCalendar.set(Calendar.MINUTE, 0);
							beginCalendar.set(Calendar.SECOND, 0);
							beginCalendar.set(Calendar.MILLISECOND, 0);

							Calendar endCalendar = dateTime.toCalendar(TimeZone.getTimeZone("GMT+08:00"));
							endCalendar.set(Calendar.HOUR_OF_DAY, endHourOfDay);
							endCalendar.set(Calendar.MINUTE, 0);
							endCalendar.set(Calendar.SECOND, 0);
							endCalendar.set(Calendar.MILLISECOND, 0);

							String beginDate = DateUtil.getDatetime(beginCalendar.getTime());
							List<HmIotEquipmentLogEntity> beginExistsList = hmIotEquipmentLogMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentLogEntity>().eq(HmIotEquipmentLogEntity::getProductId, productId).eq(HmIotEquipmentLogEntity::getDateTime, beginDate));
							if (ObjectUtil.isEmpty(beginExistsList) || beginExistsList.size() <= 0) {
								// 设备行为日志
								logEntity = new HmIotEquipmentLogEntity();
								logEntity.setProductId(productId);
								logEntity.setContent(entity.getDeviceName() + " Device connect");
								logEntity.setTime(beginDate);
								logEntity.setResult("SUCC");
								logEntity.setScene("STATUS");
								logEntity.setUserid("1");
								logEntity.setCreateBy(SecurityUtil.getUser().getSourceId());
								logEntity.setUpdateBy(SecurityUtil.getUser().getSourceId());
								hmIotEquipmentLogMapper.insert(logEntity);
							}
							String endDate = DateUtil.getDatetime(endCalendar.getTime());
							List<HmIotEquipmentLogEntity> endExistsList = hmIotEquipmentLogMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentLogEntity>().eq(HmIotEquipmentLogEntity::getProductId, productId).eq(HmIotEquipmentLogEntity::getDateTime, endDate));
							if (ObjectUtil.isEmpty(endExistsList) || endExistsList.size() <= 0) {
								logEntity = new HmIotEquipmentLogEntity();
								logEntity.setProductId(productId);
								logEntity.setContent(entity.getDeviceName() + " Device disconnect");
								logEntity.setTime(endDate);
								logEntity.setResult("SUCC");
								logEntity.setScene("STATUS");
								logEntity.setUserid("1");
								logEntity.setCreateBy(SecurityUtil.getUser().getSourceId());
								logEntity.setUpdateBy(SecurityUtil.getUser().getSourceId());
								hmIotEquipmentLogMapper.insert(logEntity);
							}
							count++;
							if(count >= size){
								break;
							}
						}
					}
					if(count >= size){
						break;
					}
				}
			}
		}
	}

	private void batchGenerationContextLogByProductId(String productId, String beginTime, String endTime, Integer current, Integer pageSize){
		try {
			TimeInterval timer = cn.hutool.core.date.DateUtil.timer();
			IPage<HmIotEquipmentEntity> page = new Page<>(current, pageSize);
			IPage<HmIotEquipmentEntity> equipmentEntityIPage = hmIotEquipmentMapper.selectPage(page, new LambdaQueryWrapper<HmIotEquipmentEntity>().eq(HmIotEquipmentEntity::getProductId, productId).in(HmIotEquipmentEntity::getFrequency, "10s", "1m", "10m", "30m", "60m"));
//		List<HmIotEquipmentEntity> equipmentEntityList = hmIotEquipmentMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentEntity>().eq(HmIotEquipmentEntity::getProductId, productId).in(HmIotEquipmentEntity::getFrequency, "10s", "1m", "10m", "30m", "60m"));
			if (ObjectUtil.isNotEmpty(equipmentEntityIPage) && equipmentEntityIPage.getRecords().size() > 0) {
				HmIotEquipmentEntity entity = equipmentEntityIPage.getRecords().get(0);
//			for(HmIotEquipmentEntity entity: equipmentEntityIPage.getRecords()){
				// 只有导入的设备数据才根据规则生成日志，双跨之用
				if (ObjectUtil.isNotEmpty(entity.getDataFlag()) && entity.getDataFlag().intValue() == 1) {
					batchGenerationContextLogByProductIdWithFrequency(entity, beginTime, endTime, current * pageSize);
				}
//			}
			}
			log.info("调用humi-app-tripart/manager/equipment/queryContextLog接口，根据产品【{}】批量生成【{}~{}】设备内容日志，耗时【{}】", productId, beginTime, endTime, cn.hutool.core.date.DateUtil.formatBetween(timer.intervalRestart()));
		}catch(Exception ex){
			log.error("根据产品【{}】批量生成【{}~{}】设备内容日志，异常：{}", productId, beginTime, endTime, ex);
		}
	}

	public void batchGenerationContextLogByProductIdWithFrequency(HmIotEquipmentEntity entity, String beginDateTime, String endDateTime, Integer size){
		TimeInterval timer = cn.hutool.core.date.DateUtil.timer();
		// 获得查询开始时间和查询结束时间所有天的日期
		Date beginDate = DateUtil.parseDatetime(beginDateTime);
		Date endDate = DateUtil.parseDatetime(endDateTime);
		List<DateTime> dateList = cn.hutool.core.date.DateUtil.rangeToList(beginDate, endDate, DateField.DAY_OF_YEAR);
		if(ObjectUtil.isNotEmpty(entity.getWorkTime())){
			// 获取每台设备每天的运行开始时间和运行结束时间
			int beginHourOfDay = Integer.valueOf(entity.getWorkTime().split("-")[0]).intValue();
			int endHourOfDay = Integer.valueOf(entity.getWorkTime().split("-")[1]).intValue();
			if(ObjectUtil.isNotEmpty(dateList) && dateList.size() > 0) {
				Integer count = 0;
				int totalDay = dateList.size();
				DateTime firstDateTime = dateList.get(0);
				DateTime lastDateTime = dateList.get(totalDay - 1);
				for(int n = 0; n < dateList.size(); n ++){
					DateTime dateTime = dateList.get(n);
					if(cn.hutool.core.date.DateUtil.isSameDay(firstDateTime.toJdkDate(), dateTime.toJdkDate())){
						if(beginDate.getHours() > beginHourOfDay){
							beginHourOfDay = beginDate.getHours();
						}
					}
					if(cn.hutool.core.date.DateUtil.isSameDay(lastDateTime.toJdkDate(), dateTime.toJdkDate())){
						if(beginDate.getHours() > beginHourOfDay){
							beginHourOfDay = beginDate.getHours();
							endHourOfDay = endDate.getHours();
						}
					}
					Calendar itemBeginCalendar = dateTime.toCalendar(TimeZone.getTimeZone("GMT+08:00"));
					itemBeginCalendar.set(Calendar.HOUR_OF_DAY, beginHourOfDay);

					Calendar itemEndCalendar = dateTime.toCalendar(TimeZone.getTimeZone("GMT+08:00"));
					itemEndCalendar.set(Calendar.HOUR_OF_DAY, endHourOfDay);

					// 根据每台设备采集信息频率，获取每台设备运行开始时间至运行结束时间间的所有时间列表
					if(ObjectUtil.isNotEmpty(entity.getFrequency())) {
						if(entity.getFrequency().equals("10s")) {

							itemBeginCalendar.set(Calendar.MINUTE, beginDate.getMinutes());
							itemBeginCalendar.set(Calendar.SECOND, CommonUtil.getTotalTen(beginDate.getSeconds()));
							itemBeginCalendar.set(Calendar.MILLISECOND, 0);
							String itemBeginDateTime = DateUtil.getDatetime(itemBeginCalendar.getTime());

							itemEndCalendar.set(Calendar.MINUTE, endDate.getMinutes());
							itemEndCalendar.set(Calendar.SECOND, CommonUtil.getTotalTen(endDate.getSeconds()));
							itemEndCalendar.set(Calendar.MILLISECOND, 0);
							String itemEndDateTime = DateUtil.getDatetime(itemEndCalendar.getTime());

							List<DateTime> tenSecdateList = CollUtil.newArrayList((Iterator<DateTime>) new DateRange(DateUtil.parseDatetime(itemBeginDateTime), DateUtil.parseDatetime(itemEndDateTime), DateField.SECOND, 10));
							count = equipmentFrequencyDateList(entity, tenSecdateList, count, size);
						}else if(entity.getFrequency().equals("1m")){

							itemBeginCalendar.set(Calendar.MINUTE, beginDate.getMinutes());
							itemBeginCalendar.set(Calendar.SECOND, 0);
							itemBeginCalendar.set(Calendar.MILLISECOND, 0);
							String itemBeginDateTime = DateUtil.getDatetime(itemBeginCalendar.getTime());

							itemEndCalendar.set(Calendar.MINUTE, endDate.getMinutes());
							itemEndCalendar.set(Calendar.SECOND, 0);
							itemEndCalendar.set(Calendar.MILLISECOND, 0);
							String itemEndDateTime = DateUtil.getDatetime(itemEndCalendar.getTime());

							List<DateTime> tenSecdateList = CollUtil.newArrayList((Iterator<DateTime>) new DateRange(DateUtil.parseDatetime(itemBeginDateTime), DateUtil.parseDatetime(itemEndDateTime), DateField.MINUTE, 1));
							count = equipmentFrequencyDateList(entity, tenSecdateList, count, size);
						}else if(entity.getFrequency().equals("10m")){

							itemBeginCalendar.set(Calendar.MINUTE, CommonUtil.getTotalTen(beginDate.getMinutes()));
							itemBeginCalendar.set(Calendar.SECOND, 0);
							itemBeginCalendar.set(Calendar.MILLISECOND, 0);
							String itemBeginDateTime = DateUtil.getDatetime(itemBeginCalendar.getTime());

							itemEndCalendar.set(Calendar.MINUTE, CommonUtil.getTotalTen(endDate.getMinutes()));
							itemEndCalendar.set(Calendar.SECOND, 0);
							itemEndCalendar.set(Calendar.MILLISECOND, 0);
							String itemEndDateTime = DateUtil.getDatetime(itemEndCalendar.getTime());

							List<DateTime> tenSecdateList = CollUtil.newArrayList((Iterator<DateTime>) new DateRange(DateUtil.parseDatetime(itemBeginDateTime), DateUtil.parseDatetime(itemEndDateTime), DateField.MINUTE, 10));
							count = equipmentFrequencyDateList(entity, tenSecdateList, count, size);
						}else if(entity.getFrequency().equals("30m")){

							itemBeginCalendar.set(Calendar.MINUTE, 0);
							itemBeginCalendar.set(Calendar.SECOND, 0);
							itemBeginCalendar.set(Calendar.MILLISECOND, 0);
							String itemBeginDateTime = DateUtil.getDatetime(itemBeginCalendar.getTime());

							itemEndCalendar.set(Calendar.MINUTE, 0);
							itemEndCalendar.set(Calendar.SECOND, 0);
							itemEndCalendar.set(Calendar.MILLISECOND, 0);
							String itemEndDateTime = DateUtil.getDatetime(itemEndCalendar.getTime());

							List<DateTime> tenSecdateList = CollUtil.newArrayList((Iterator<DateTime>) new DateRange(DateUtil.parseDatetime(itemBeginDateTime), DateUtil.parseDatetime(itemEndDateTime), DateField.MINUTE, 30));
							count = equipmentFrequencyDateList(entity, tenSecdateList, count, size);
						}else if(entity.getFrequency().equals("60m")){

							itemBeginCalendar.set(Calendar.MINUTE, 0);
							itemBeginCalendar.set(Calendar.SECOND, 0);
							itemBeginCalendar.set(Calendar.MILLISECOND, 0);
							String itemBeginDateTime = DateUtil.getDatetime(itemBeginCalendar.getTime());

							itemEndCalendar.set(Calendar.MINUTE, 0);
							itemEndCalendar.set(Calendar.SECOND, 0);
							itemEndCalendar.set(Calendar.MILLISECOND, 0);
							String itemEndDateTime = DateUtil.getDatetime(itemEndCalendar.getTime());

							List<DateTime> tenSecdateList = CollUtil.newArrayList((Iterator<DateTime>) new DateRange(DateUtil.parseDatetime(itemBeginDateTime), DateUtil.parseDatetime(itemEndDateTime), DateField.MINUTE, 60));
							count = equipmentFrequencyDateList(entity, tenSecdateList, count, size);
						}
					}
					if(count.intValue() >= size.intValue()){
						break;
					}
				}
			}
			log.info("根据规则批量生成设备【{}】【{}~{}】【{}】的内容日志，耗时【{}】", entity.getDeviceName(), beginDateTime, endDateTime, entity.getFrequency(), cn.hutool.core.date.DateUtil.formatBetween(timer.intervalRestart()));
		}
	}

	private Integer equipmentFrequencyDateList(HmIotEquipmentEntity entity, List<DateTime> dateList, Integer count, Integer size){
		HmIotEquipmentLogEntity itemEntity = null;
		List<HmIotEquipmentLogEntity> logEntityList = new ArrayList<>();
		for(DateTime itemDateTime : dateList){
			HmIotEquipmentLogEntity existsEntity = hmIotEquipmentLogMapper.selectOne(
					new LambdaQueryWrapper<HmIotEquipmentLogEntity>()
							.eq(HmIotEquipmentLogEntity::getType, 2)
							.eq(HmIotEquipmentLogEntity::getProductId, entity.getProductId())
							.eq(HmIotEquipmentLogEntity::getDeviceName, entity.getDeviceNameUuid())
							.eq(HmIotEquipmentLogEntity::getDateTime, itemDateTime));
			if(ObjectUtil.isEmpty(existsEntity)){
				String payload = Base64.encode(getEquipmentPayload(entity))+"}";
				itemEntity = new HmIotEquipmentLogEntity();
				itemEntity.setId(IdWorker.getIdStr());
				itemEntity.setType("2");
				itemEntity.setProductId(entity.getProductId());
				itemEntity.setDeviceName(entity.getDeviceNameUuid());
				itemEntity.setRequestId(cn.hutool.core.util.RandomUtil.randomNumbers(18));
				itemEntity.setSrcName(itemEntity.getProductId()+'/'+itemEntity.getDeviceName());
				itemEntity.setTopic(itemEntity.getProductId()+"/"+itemEntity.getDeviceName()+'/'+itemEntity.getRequestId());
				itemEntity.setPayload(payload);
				itemEntity.setPayloadFmtType("json");
				itemEntity.setDateTime(itemDateTime.toString());
				itemEntity.setUin("1");
				itemEntity.setCreateBy(SecurityUtil.getUser().getSourceId());
				itemEntity.setUpdateBy(SecurityUtil.getUser().getSourceId());
				logEntityList.add(itemEntity);
				count ++;
				if(count.intValue() >= size.intValue()){
					break;
				}
			}
		}
		if(ObjectUtil.isNotEmpty(logEntityList) && logEntityList.size() > 0){
			batchSaveItem(logEntityList);
		}
		return count;
	}

	private void batchSaveItem(List<HmIotEquipmentLogEntity> contextEntityList){
		managerEquipmentLogMapper.batchSave(contextEntityList);
	}

	private String getEquipmentPayload(HmIotEquipmentEntity entity){
		List<HmIotEquipmentParameterEntity> parameterEntityList = hmIotEquipmentParameterMapper.selectList(new LambdaQueryWrapper<HmIotEquipmentParameterEntity>().eq(HmIotEquipmentParameterEntity::getTempletId, entity.getTempletId()));
		if(ObjectUtil.isNotEmpty(parameterEntityList) && parameterEntityList.size() > 0){
			Map<String, String> payloadMap = Maps.newHashMap();
			for(HmIotEquipmentParameterEntity parameterEntity: parameterEntityList){
				Double min = new Double(parameterEntity.getParameterMin());
				Double max = new Double(parameterEntity.getParameterMax());
				if("odo".equals(parameterEntity.getParameterCode())){
					Integer odoValue = RedisCacheHelper.getValue(CommonUtil.IOT_EQUIPMENT_PARAMETER_ODO_KEY+"_"+entity.getId());
					if(ObjectUtil.isNotEmpty(odoValue)){
						odoValue += RandomUtil.randomInt(0, 50);
						payloadMap.put(parameterEntity.getParameterCode(), String.valueOf(odoValue));
						RedisCacheHelper.setValue(CommonUtil.IOT_EQUIPMENT_PARAMETER_ODO_KEY+"_"+entity.getId(), odoValue);
					}else{
						odoValue = Double.valueOf(RandomUtil.randomDouble(min, max)).intValue();
						payloadMap.put(parameterEntity.getParameterCode(), String.valueOf(odoValue));
						RedisCacheHelper.setValue(CommonUtil.IOT_EQUIPMENT_PARAMETER_ODO_KEY+"_"+entity.getId(), odoValue);
					}
				}else{
					payloadMap.put(parameterEntity.getParameterCode(), String.valueOf(Double.valueOf(RandomUtil.randomDouble(min, max)).intValue()));
				}
			}
			return JSON.toJSONString(payloadMap);
		}
		return "";
	}
}