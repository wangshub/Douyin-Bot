package com.humi.app.tripart.manager.dao;

import com.humi.app.tripart.common.entity.HmIotEquipmentLogEntity;
import com.humi.app.tripart.manager.model.equipmentlog.EquipmentBehaviorLogResponseBean;
import com.humi.app.tripart.manager.model.equipmentlog.EquipmentContextLogResponseBean;
import com.humi.app.tripart.manager.model.equipmentlog.SearchEquipmentLogRequestBean;
import com.humi.cloud.mybatis.support.model.Page;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * @Author Josh
 * <pre>
 * <b></b>
 * <b>Description:</b>
 * 	---------------------
 * <b>Author:</b> shihu@360humi.com
 * <b>Date:</b> 2020/11/09 10:29
 * <b>Copyright:</b> Copyright 2017-2019 www.360humi.com Technology Co., Ltd. All rights reserved.
 * <b>Changelog:</b>
 *   Ver   		Date                    Author               	 Detail
 *   ----------------------------------------------------------------------
 *   1.0   2020/11/09 10:29    shihu@360humi.com     new file.
 * </pre>
 */
public interface ManagerEquipmentLogMapper {

    List<EquipmentBehaviorLogResponseBean> searchEquipmentBehaviorLogPage(Page<EquipmentBehaviorLogResponseBean, SearchEquipmentLogRequestBean> page);

    List<EquipmentContextLogResponseBean> searchEquipmentContextLogPage(Page<EquipmentContextLogResponseBean, SearchEquipmentLogRequestBean> page);

    void batchSave(@Param(value = "entityList") List<HmIotEquipmentLogEntity> entityList);
}
