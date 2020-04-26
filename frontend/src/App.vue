<template>
  <div id="app">
    <router-view />
    <el-backtop :visibility-height="100">
      <el-tooltip placement="top" content="上车吧！骚年">
        <svg-icon icon-class="rocket" style="width: 40px; height: 40px;" />
      </el-tooltip>
    </el-backtop>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>
