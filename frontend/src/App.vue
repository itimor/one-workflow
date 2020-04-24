<template>
  <div id="app">
    <router-view/>
    <el-tooltip placement="top" content="上车吧！骚年">
      <back-to-top :visibility-height="10" :back-position="50" transition-name="fade"/>
    </el-tooltip>
  </div>
</template>

<script>
  import BackToTop from '@/components/BackToTop'

  export default {
    name: 'App',
    components: {BackToTop}
  }
</script>
