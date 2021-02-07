<template>
  <div id="app">
    <router-view />
    <el-backtop :visibility-height="100">
      <el-tooltip placement="top" content="ちょっと待って">
        <div class="shake shake-crazy">
          <svg-icon icon-class="rocket" style="width: 40px; height: 40px;" />
        </div>
      </el-tooltip>
    </el-backtop>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>
