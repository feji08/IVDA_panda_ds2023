<template>
  <div class="graph-container" ref="container">
    <NetWorkGraph :nodes="$props.nodes" :edges="$props.edges" :layouts="$props.layouts"
                  :overview=true :scaleRatio=0.5 :rectangle=rectangle :indicator="$props.indicator"
                  @update-focus="handleUpdateFocus"
                  @update-viewBox="handleUpdateViewBox" />
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
  components: { NetWorkGraph},
  props: ["indicator","nodes","edges","layouts"],
  data() {
    return {
      rectanglePosition: { left: 20, top: 20 },
      rectangleWidth: 90,
      rectangleHeight: 60,
      isDragging: false,
      startX: 0,
      startY: 0,
      ContainerWidth: 0,
      ContainerHeight: 0,
      rectangle: {left:0,top:0,right:0,bottom:0},
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
        this.rectangle = {
          left:this.rectanglePosition.left,
          top:this.rectanglePosition.top,
          right:this.rectanglePosition.left+this.rectangleWidth,
          bottom:this.rectanglePosition.top+this.rectangleHeight,
        }
      }
    },
    stopDragging() {
      this.isDragging = false;
    },
    handleUpdateFocus(focus){
      // console.log(focus)
      this.rectanglePosition.left = focus.x-this.rectangleWidth/2;
      this.rectanglePosition.top = focus.y-this.rectangleHeight/2;
      this.rectangle = {
        left:focus.x-this.rectangleWidth/2,
        top:focus.y-this.rectangleHeight/2,
        right:focus.x+this.rectangleWidth/2,
        bottom:focus.y+this.rectangleHeight/2,
      }
    },
    handleUpdateViewBox(newViewBox){
      this.$emit('updateViewBox', newViewBox);
    }
  },
};
</script>

<style>
.graph-container {
  height: 100%;
}

.draggable-rectangle {
  position: absolute;
  background: rgba(192, 214, 223, 0.34);
  cursor: grab;
}
</style>