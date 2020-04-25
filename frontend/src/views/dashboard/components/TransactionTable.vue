<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="Order_No" min-width="200">
      <template slot-scope="{row}">{{ row.order_no | orderNoFilter }}</template>
    </el-table-column>
    <el-table-column label="Price" width="195" align="center">
      <template slot-scope="{row}">¥{{ row.price | toThousandFilter }}</template>
    </el-table-column>
    <el-table-column label="Status" width="100" align="center">
      <template slot-scope="{row}">
        <el-tag :type="row.status | statusFilter">{{ row.status }}</el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: "success",
        pending: "danger"
      };
      return statusMap[status];
    },
    orderNoFilter(str) {
      return String(str).substring(0, 30);
    }
  },
  data() {
    return {
      list: [
        { order_no: 1, price: "111", status: "success" },
        { order_no: 1, price: "222", status: "pending" },
        { order_no: 2, price: "333", status: "pending" }
      ]
    };
  },
  created() {
  },
  methods: {}
};
</script>
