<template>
  <div class="filter-container">
    <a>{{listQuery.workflow}}</a>
  </div>
</template>

<script>
import { customfield, state, transition, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "wfconf",

  components: { Pagination },
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      tempRoute: {},
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
        workflow: undefined
      },
      customfield_list: [],
      customfield_total: 0,
      customfield_listLoading: false
    };
  },

  created() {
    this.listQuery.workflow = this.$route.params && this.$route.params.id;
    this.getCustomfieldList();
    this.tempRoute = Object.assign({}, this.$route);
    this.setTagsViewTitle()
    this.setPageTitle()
  },
  methods: {
    getCustomfieldList() {
      this.customfield_listLoading = true;
      customfield.requestGet(this.listQuery).then(response => {
        this.customfield_list = response.results;
        this.customfield_total = response.count;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.getCustomfieldList();
    },
    setTagsViewTitle(id) {
      const title = "工作流配置";
      const route = Object.assign({}, this.tempRoute, {
        title: `${title}-${this.listQuery.workflow}`
      });
      this.$store.dispatch("tagsView/updateVisitedView", route);
    },
    setPageTitle() {
      const title = "工作流配置";
      document.title = `${title} - ${this.listQuery.workflow}`;
    }
  }
};
</script>
