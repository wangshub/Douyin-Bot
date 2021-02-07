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
@TableName("hm_iot_equipment_log")
@EqualsAndHashCode(callSuper=false)
public class HmIotEquipmentLogEntity extends Entity<HmIotEquipmentLogEntity> {

    private static final long serialVersionUID = 1L;

    /**
     * 设备日志类型 1-行为日志 2-内容日志 3-设备日志
     */
    private String type;

    /**
     * 产品id
     */
    private String productId;

    /**
     * 设备名称
     */
    private String deviceName;

    /**
     * 请求id
     */
    private String requestId;

    /**
     * 源名称
     */
    private String srcName;

    /**
     * topic
     */
    private String topic;

    /**
     * payload
     */
    private String payload;

    /**
     * payload_fmt_type
     */
    private String payloadFmtType;

    /**
     * date_time
     */
    private String dateTime;

    /**
     * uin
     */
    private String uin;

    /**
     * 设备日志内容
     */
    private String content;

    /**
     * 日志生成时间
     */
    private String time;

    /**
     * 结果
     */
    private String result;

    /**
     * 类别
     */
    private String scene;

    /**
     * 用户id
     */
    private String userid;
}
