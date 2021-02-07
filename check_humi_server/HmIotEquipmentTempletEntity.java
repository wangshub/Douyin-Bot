package com.humi.app.tripart.common.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.humi.cloud.mybatis.support.model.Entity;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * <pre>
 * <b>Description: coding_team</b>
 * <b>@Author: autoCode v1.0</b>
 * <b>Date: 2020-12-02</b>
 * </pre>
 */
@Data
@TableName("hm_iot_equipment_templet")
@EqualsAndHashCode(callSuper=false)
public class HmIotEquipmentTempletEntity extends Entity<HmIotEquipmentTempletEntity> {

    private static final long serialVersionUID = 1L;

    /**
     * 用户id
     */
    private String userId;

    /**
     * 模板名称
     */
    private String templetName;

    /**
     * 模板描述
     */
    private String templetDesc;
}
