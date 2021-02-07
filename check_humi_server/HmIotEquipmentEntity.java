package com.humi.app.tripart.common.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.humi.cloud.mybatis.support.model.Entity;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 
 * <pre>
 * <b>Description: coding_team</b> 
 * <b>Author: autoCode v1.0</b>
 * <b>Date: 2020-07-14</b>
 * </pre>
 */
 
@Data
@TableName("hm_iot_equipment")
@EqualsAndHashCode(callSuper=false)
public class HmIotEquipmentEntity extends Entity<HmIotEquipmentEntity> {

  	private static final long serialVersionUID = 1L;
  
  	/** 租户id */
	protected String lessee;
	
  	/** 用户id */
	protected String userId;
	
  	/** 产品id */
	protected String productId;
	
  	/** 状态  0 离线  1在线  3 未激活 */
	protected Integer state;
	
  	/** 设备名称 */
	protected String deviceName;

  	/** 设备名称uuid */
	protected String deviceNameUuid;

	/** 描述 */
	protected String description;

	/** 设备私钥 0 未下载 1已下载 */
	protected Integer certState;

	/** 最后上线时间 */
	protected Long loginTime;

  	/** 对称加密密钥，base64编码。采用对称加密时返回该参数 */
	protected String devicePsk;
	
  	/** 设备证书，用于 TLS 建立链接时校验客户端身份。采用非对称加密时返回该参数 */
	protected String deviceCert;

  	/** 设备私钥，用于 TLS 建立链接时校验客户端身份，腾讯云后台不保存，请妥善保管。采用非对称加密时返回该参数 */
	protected String devicePrivateKey;

  	/** LoRa设备的DevEui，当设备是LoRa设备时，会返回该字段 */
	protected String loraDevEui;

  	/** LoRa设备的MoteType，当设备是LoRa设备时，会返回该字段 */
	protected Integer loraMoteType;

  	/** LoRa设备的AppKey，当设备是LoRa设备时，会返回该字段 */
	protected String loraAppKey;

  	/** LoRa设备的NwkKey，当设备是LoRa设备时，会返回该字段 */
	protected String loraNwkKey;

  	/** 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId */
	protected String requestId;

  	/** 返回的json */
	protected String jsonData;

  	/** 行业id */
	protected String industryId;

  	/** 设备种类id */
	protected String equipmentBreedId;

	/** 设备类型id */
	protected String equipmentTypeId;

	/** 协议类型 */
	protected String protocolType;

  	/** 位置  */
	protected String position;

	/** 省 名称  */
	protected String provinceName;

	/** 区 名称  */
	protected String city;

  	/** 是否绑定 1是 2否  */
	protected Integer isBinding;

  	/** 绑定的设备uuid  */
	protected String gatewayDeviceName;

  	/** 连接类型 1设备  2传感器  */
	protected Integer connectType;

  	/** 传感器类型 1 数值型 2 开关型（可操作）3 开关型（不可操作）4定位型 5字符串型  */
	protected Integer sensorType;

  	/** 传感器小数类型 1(0位小数)  2(1位小数)  3(2位小数) 4(3位小数) 5(4位小数)  */
	protected Integer sensorDecimalsType;

	/** 工作时间，0-24表示24小时运行，9-20表示9点-20点运行 */
	protected String workTime;

	/** 采集频率，10s表示10秒每次，10m表示10分钟每次 */
	protected String frequency;

	/** 模板id，对应hm_iot_equipment_templet表的id */
	protected String templetId;

	/** 数据标识，用于区分导入数据、手工录入数据 */
	protected Integer dataFlag;
}