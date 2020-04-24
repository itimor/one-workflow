<template>
  <el-row class="dashboard-editor-container">
    <panel-group/>
  </el-row>
</template>

<script>
  import PanelGroup from './components/PanelGroup'

  export default {
    name: 'DashboardAdmin',
    components: {
      PanelGroup,
    },
    data() {
      return {
      }
    },
    computed: {},
    methods: {
    }
  }
</script>

<style lang="scss" scoped>
  .dashboard-editor-container {
    padding: 32px;
    background-color: rgb(240, 242, 245);
    position: relative;

    .home-middle {
      margin-bottom: 20px;

      .info-container {
        line-height: 200px;

        .display_name {
          font-size: 32px;
          line-height: 48px;
          color: #40c9c6;
          position: absolute;
        }

        .introduction {
          font-size: 24px;
          font-style: italic;
          line-height: 32px;
          color: #c0c4cc;
        }
      }

      .emptyGif {
        display: block;
        width: 60%;
        margin: 0 auto;
      }
    }

    .chart-wrapper {
      background: #fff;
      padding: 16px 16px 0;
      margin-bottom: 32px;
    }
  }
</style>
