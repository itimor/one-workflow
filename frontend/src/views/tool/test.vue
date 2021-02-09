<template>
  <div>
    <bpmn-modeler
      ref="refNode"
      :xml="xml"
      :users="users"
      :groups="groups"
      :categorys="categorys"
      :is-view="false"
      @save="save"
    />
  </div>
</template>

<script>
import bpmnModeler from "workflow-bpmn-modeler";
import { workflowbpmn } from "@/api/all";

export default {
  components: {
    bpmnModeler,
  },
  data() {
    return {
      list: [],
      total: 0,
      xml: "", // 后端查询到的xml
      users: [
        { name: "张三", id: "zhangsan" },
        { name: "李四", id: "lisi" },
        { name: "王五", id: "wangwu" },
      ],
      groups: [
        { name: "web组", id: "web" },
        { name: "java组", id: "java" },
        { name: "python组", id: "python" },
      ],
      categorys: [
        { name: "OA", id: "oa" },
        { name: "财务", id: "finance" },
      ],
    };
  },
  created() {
    this.getModelDetail();
  },
  methods: {
    getModelDetail() {
      // 发送请求，获取xml
      workflowbpmn.requestGet().then((response) => {
        this.list = response.results;
        this.xml = this.list[0].xml;
        this.total = response.count;
      });
    },
    save(data) {
      console.log(data); 
    },
  },
};
</script>