<template>
  <div class="filter-container">
    <a>{{wfdata.name}}</a>
  </div>
</template>

<script>
import { workflow, customfield, state, transition, auth } from "@/api/all";
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
      wfdata: {},
      customfield_list: [],
      customfield_total: 0,
      customfield_listLoading: false
    };
  },

  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.tempRoute = Object.assign({}, this.$route);
  },
  methods: {
    fetchData(id) {
      this.listQuery.workflow = id;
      const params = {
        id: id
      };
      workflow.requestGet(params).then(response => {
        this.wfdata = response.results[0];

        this.setTagsViewTitle();
        this.setPageTitle();
      });
    },
    getCustomfieldList() {
      this.customfield_listLoading = true;
      this.listQuery.workflow = id;
      customfield.requestGet(this.listQuery).then(response => {
        this.customfield_list = response.results;
        this.customfield_total = response.count;
        this.customfield_listLoading = false;

        this.setTagsViewTitle();
        this.setPageTitle();
      });
    },
    handleFilter() {
      this.getCustomfieldList();
    },
    setTagsViewTitle() {
      const title = this.wfdata.name;
      const route = Object.assign({}, this.tempRoute, {
        title: `${title} - 配置`
      });
      this.$store.dispatch("tagsView/updateVisitedView", route);
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 配置`;
    }
  }
};
</script>
