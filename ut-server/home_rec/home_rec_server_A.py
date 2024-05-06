import os
import pickle
import time

import sys
sys.path.append("..")

import numpy as np

from conf import settings
from dto.home_rec_v8_pb2 import HomeRankV8Request, HomeRankV8Response
from utils.logger_helper import logger
from utils import multi_proc_service_v3
from utils.multi_proc_service_v3 import BaseService
from utils.oss_util import ProcessHotOssDir
from .home_rec_offline.model.ESMM_v8_model import ESMMV8HyperParams, ESMMV8ModelTrainer
from .home_rec_offline.config.ESMM_v8_config import user_features, item_features, context_features


class HomeRecServerA():
    def init(self):
        logger.info("Start to init HomeRecServerA")
        self.model = None
        self.user_list = tuple(user_features.keys())
        self.item_list = tuple(item_features.keys())
        self.context_list = tuple(context_features.keys())
        self.hot_model = ProcessHotOssDir(settings["home_rec_mlt"]["v3_1"]["oss_dir"],
                                          callback=self.load_model,
                                          passive=True)
        self.monitor_list.append(self.hot_model)

    def load_model(self, model_file):
        logger.info(f"开始载入模型  HomeRecMLT ServerA 路径为 {model_file}, 模型版本 ESMM_v8")
        hp = ESMMV8HyperParams(
            batch_size=4096,
            epochs=3,
            optimizer="Adam_0.0003",
            dnn_units=[512, 256, 128, 64],
            dnn_activation="relu",
            l2_reg=0.0000025,
            att_units=[64, 32, 1],
            use_bn=True,
            dropout=0.0,
            embedding_initializer="glorot_normal"
        )
        trainer = ESMMV8ModelTrainer(None, hp)
        model = trainer.build_model()
        with open(os.path.join(model_file, "checkpoint.pkl"), "rb") as f:
            checkpoint = pickle.load(f)
        model.set_weights(checkpoint["weights"])
        self.model = model
        logger.info("模型载入完毕")
        self._warm_up()

    def _warm_up(self):
        rank_request = HomeRankV8Request()
        rank_request.user_feature.gender = "男"
        rank_request.user_feature.school = "同济大学"
        rank_request.user_feature.school_major = "材料科学与工程"
        rank_request.user_feature.school_type = "双一流"
        rank_request.user_feature.edu_work_status = 2
        rank_request.user_feature.work_status_detail = 3
        rank_request.user_feature.career_job1_1 = "11226"
        rank_request.user_feature.career_job1_2 = "11240"
        rank_request.user_feature.career_job1_3 = "11248"
        rank_request.user_feature.career_job2_2 = "11200"
        rank_request.user_feature.career_job2_3 = "11002"
        rank_request.user_feature.career_job3_2 = "11200"
        rank_request.user_feature.career_job3_3 = "11003"
        rank_request.user_feature.work_year = 5
        rank_request.user_feature.edu_level = "学士"
        hist_entity_id = ["80001117703", "80001118031", "80001115261", "80001115002", "80001114348", "80001111721",
                          "80001111920", "740001602617", "740001598629", "740001585055", "740001585055", "740001597732",
                          "740001599146", "740001599146", "740001587173", "740001583468", "740001592102"]
        default_hist_entity_id = ["<nan>" for _ in range(20 - 17)]
        rank_request.user_feature.hist_entity_id.extend(hist_entity_id + default_hist_entity_id)
        rank_request.user_feature.max_len = 17
        rank_request.user_feature.comment_list_entity_id.extend(
            ["80001117703", "80001115261", "<nan>", "<nan>", "<nan>", "<nan>", "<nan>", "<nan>", "<nan>", "<nan>"])
        rank_request.user_feature.comment_list_max_len = 2
        rank_request.user_feature.expo_not_click_entity_id.extend(["10000000000", "<nan>", "<nan>", "<nan>", "<nan>",
                                                                   "<nan>", "<nan>", "<nan>", "<nan>", "<nan>", "<nan>",
                                                                   "<nan>", "<nan>", "<nan>", "<nan>", "<nan>", "<nan>",
                                                                   "<nan>", "<nan>", "<nan>"])
        rank_request.user_feature.expo_not_click_max_len = 1
        rank_request.user_feature.uid = "987571681"
        rank_request.user_feature.short_term_companies.extend(["1", "2", "3", "10000000000", "10000000000"])
        rank_request.user_feature.short_term_companies_weights.extend([0.1, 0.2, 0.3, 0.0, 0.0])

        for i in range(150):
            item_feature = rank_request.item_feature.add()
            item_feature.reply_number = 0
            item_feature.like_number = 0
            item_feature.view_number = 9
            item_feature.post_module = 0
            item_feature.content_mode = 0
            item_feature.content_topic.extend(["10000000000", "<nan>", "<nan>"])
            item_feature.topic_max_len = 1
            item_feature.taxonomy1 = "10016"
            item_feature.taxonomy2 = "0"
            item_feature.form = 0
            item_feature.ctr = 3
            item_feature.ctr_3 = 1
            item_feature.ctr_7 = 1
            item_feature.career_job_ctr = 2
            item_feature.manual_career_job_1 = "11226"
            item_feature.manual_career_job_2 = "0"
            item_feature.day_delta = 1
            item_feature.company_keyword.extend(["10000000000", "<nan>", "<nan>"])
            item_feature.company_keyword_max_len = 1
            item_feature.entity_id = "740001603930"

            item_feature.author_uid = "123456789"
            item_feature.author_gender = "男"
            item_feature.author_career_job1_1 = "11226"
            item_feature.author_career_job1_2 = "11240"
            item_feature.author_career_job1_3 = "11248"
            item_feature.author_school = "合肥工业大学"
            item_feature.author_school_major = "管理科学与工程"
            item_feature.author_school_type = "211"
            item_feature.author_edu_level = "硕士"
            item_feature.author_edu_work_status = 1
            item_feature.author_work_year = 3

        self.work(rank_request.SerializeToString())

    def work(self, request_pb):
        start_time = time.time()
        rank_request = HomeRankV8Request()
        rank_request.ParseFromString(request_pb)
        size = len(rank_request.item_feature)
        assert size > 0
        logger.info(f"候选物料的数量为 {size}")
        all_features = {k: np.array([getattr(rank_request.user_feature, k) for _ in range(size)])
                        for k in self.user_list}
        all_features.update({k: np.array([getattr(rank_request.item_feature[idx], k)
                                          for idx in range(size)]) for k in self.item_list})

        logger.info(f"home_rec_test mlt_v1 protobuf to dict 耗时 {time.time() - start_time}")
        start_time = time.time()

        res = self.model(all_features, training=False)
        ctr = res[0].numpy()
        cvr = res[1].numpy() / ctr
        logger.info(f"home_rec_test mlt_v1 模型 耗时 {time.time() - start_time}")

        response = HomeRankV8Response()
        response.ctr_score.extend(ctr)
        response.cvr_score.extend(cvr)
        # logger.info(f"消息response: {response}")
        return response.SerializeToString()

    def run(self):
        self.init()



if __name__ == "__main__":
    ## multi_proc_service_v3.BaseHandler(HomeRecServerA, process_num=2)
    obj = HomeRecServerA()
    obj.run()
