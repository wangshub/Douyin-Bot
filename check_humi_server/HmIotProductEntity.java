package com.humi.app.tripart.common.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.humi.cloud.mybatis.support.model.Entity;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 
 * <pre>
 * <b>Description: 产品</b>
 * <b>Author: autoCode v1.0</b>
 * <b>Date: 2020-07-14</b>
 * </pre>
 */
 
@Data
@TableName("hm_iot_product")
@EqualsAndHashCode(callSuper=false)
public class HmIotProductEntity extends Entity<HmIotProductEntity> {

  	private static final long serialVersionUID = 1L;
  
  	/** 租户id */
	protected String lessee;
	
  	/** 用户id */
	protected String userId;
	
  	/** 产品名称 */
	protected String productName;

  	/** 产品名称 */
	protected String productNameUuid;
	
  	/** 产品类型 0 普通产品，2 NB-IoT产品，4 LoRa产品，3 LoRa网关产品，5 普通网关产品 默认值是0 */
	protected Integer productType;
	
  	/** 认证方式 加密类型，1表示证书认证，2表示签名认证。如不填写，默认值是1 */
	protected String encryptionType;

  	/** 数据格式 取值为json或者custom，默认值是json */
	protected String format;

	/** 产品描述 */
	protected String productDescription;

	/** 产品绑定的物模型ID，-1表示不绑定 */
	protected String modelId;

	/** 产品绑定的物模型名称 */
	protected String modelName;

	/** 绑定的网关产品id */
	protected String gatewayProductId;

	/** 是否被绑定 1 是 0否 */
	protected Integer isBinding;

	/** 模板id，对应hm_iot_equipment_templet表的id */
	protected String templetId;
}