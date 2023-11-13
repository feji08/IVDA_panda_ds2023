<template>
  <div class="graph-container" ref="container">
    <NetWorkGraph ScaleRatio="0.4" />
    <div
        class="draggable-rectangle"
        @mousedown="startDragging"
        @mousemove="handleDragging"
        @mouseup="stopDragging"
        :style="{
          left: rectanglePosition.left + 'px',
          top: rectanglePosition.top + 'px',
          width: rectangleWidth + 'px',
          height: rectangleHeight + 'px',
        }"
    ></div>
  </div>
</template>

<script>
import NetWorkGraph from './NetWorkGraph';
export default {
  components: {NetWorkGraph},
  data() {
    return {
      rectanglePosition: { left: 20, top: 20 },
      rectangleWidth: 60,
      rectangleHeight: 40,
      isDragging: false,
      startX: 0,
      startY: 0,
      ContainerWidth: 0,
      ContainerHeight: 0,
    };
  },
  mounted() {
    this.getContainerRect();
  },
  methods: {
    getContainerRect(){
      const container = this.$refs.container;
      const containerRect = container.getBoundingClientRect();
      this.ContainerWidth = containerRect.right - containerRect.left;
      this.ContainerHeight = containerRect.bottom - containerRect.top;
      console.log(`Container X: ${containerRect.left} - ${containerRect.right},
      Y: ${containerRect.top} - ${containerRect.bottom}`)
      console.log(`Width: ${this.ContainerWidth}, Height: ${this.ContainerHeight}`)
    },
    startDragging(event) {
      this.isDragging = true;
      event.preventDefault();
      //clientX/Y: based on the browser left-bottom; this.startX/Y: based on the rectangle
      this.startX = event.clientX - this.rectanglePosition.left;
      this.startY = event.clientY - this.rectanglePosition.top;
    },
    handleDragging(event) {
      event.preventDefault();
      if (this.isDragging) {
        const newLeft = event.clientX - this.startX;
        const newTop = event.clientY - this.startY;
        if (newLeft >= 0 && newLeft + this.rectangleWidth <= this.ContainerWidth) {
          this.rectanglePosition.left = newLeft;
        }
        if (newTop >= 0 && newTop + this.rectangleHeight <= this.ContainerHeight) {
          this.rectanglePosition.top = newTop;
        }
        console.log(`X: ${newLeft}, Y: ${newTop}`);
        console.log(`X: ${0} - ${this.ContainerWidth}, Y: ${0} - ${this.ContainerHeight}`)
      }
    },
    stopDragging() {
      this.isDragging = false;
    },
  },
};
</script>

<style>
.graph-container {
  height: 100%;
}

.draggable-rectangle {
  position: absolute;
  background: rgba(134, 134, 246, 0.3);
  cursor: grab;
}
</style>