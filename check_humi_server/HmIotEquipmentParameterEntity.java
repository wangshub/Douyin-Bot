package com.humi.app.tripart.common.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.humi.cloud.mybatis.support.model.Entity;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * <pre>
 * <b>Description: coding_team</b>
 * <b>Author: autoCode v1.0</b>
 * <b>Date: 2020-11-09</b>
 * </pre>
 */
@Data
@TableName("hm_iot_equipment_parameter")
@EqualsAndHashCode(callSuper=false)
public class HmIotEquipmentParameterEntity extends Entity<HmIotEquipmentParameterEntity> {

    private static final long serialVersionUID = 1L;

    /**
     * 设备种类id
     */
    private String templetId;

    /**
     * 参数名称
     */
    private String parameterName;

    /**
     * 参数英文编码
     */
    private String parameterCode;

    /**
     * 参数类型，Integer、String、Double
     */
    private String parameterType;

    /**
     * 参数单位
     */
    private String parameterUnit;

    /**
     * 参数值最小值
     */
    private String parameterMin;

    /**
     * 参数值最大值
     */
    private String parameterMax;
}
