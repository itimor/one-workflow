<template>
  <div>
    <svg-icon :icon-class="isFullscreen?'exit-fullscreen':'fullscreen'" @click="click"/>
  </div>
</template>

<script>
  import screenfull from 'screenfull'

  export default {
    name: 'Screenfull',
    data() {
      return {
        isFullscreen: false
      }
    },
    methods: {
      click() {
        if (screenfull.isEnabled) {
          this.isFullscreen = !this.isFullscreen
          screenfull.toggle();
        }
      }
    }
  }
</script>
