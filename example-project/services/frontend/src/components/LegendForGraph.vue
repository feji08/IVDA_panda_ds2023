<template>
  <div class="legend-container">
    <div class="item-container">
      <div class="dot-container">
        <div class="dot blue-dot"></div>
        <div class="label dot-label">normal attribute</div>
        <div class="dot red-dot"></div>
        <div class="label dot-label">indicator attribute</div>
      </div>
      <div class="label bottom-label">stock attributes</div>
    </div>
    <div class="item-container">
      <div class="line-container">
        <div class="label left-label">-1</div>
        <div v-for="width in [-1,-0.9, -0.8, -0.7, -0.6, -0.5, 0, 0.5, 0.6, 0.7, 0.8, 0.9]"
             :key="width" class="line" :style="getLineStyle(width)"></div>
        <div class="label right-label">1</div>
      </div>
      <div class="label bottom-label">correlation coefficient</div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    getLineStyle(width) {
      const lineWidth = 20;
      const lineHeight = 3;
      const lineColor = this.mapWidthToColor(width);
      return {
        width: `${lineWidth}px`,
        height: `${lineHeight}px`,
        backgroundColor: lineColor,
        margin: '5px 0',
      };
    },
    mapWidthToColor(width) {
      const colorMap = {
        0.9: "#023E8A",
        0.8: "#0096C7",
        0.7: "#48CAE4",
        0.6: "#ADE8F4",
        0: "#caf0f8",
        "-0.6": "#F9BD9D",
        "-0.7": "#F8AB81",
        "-0.8": "#F58A51",
        "-0.9": "#F05D0E",
        default: "#660708"
      };
      const sortedKeys = Object.keys(colorMap).map(parseFloat).sort((a, b) => b - a);
      for (let i = 0; i < sortedKeys.length; i++) {
        const currentKey = sortedKeys[i];
        if (width >= currentKey) {
          return colorMap[currentKey];
        }
      }
      return colorMap.default;
    },
  },
};
</script>

<style scoped>
.legend-container {
  display: flex;
  justify-content: space-between;
}
.item-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right:40px;
}
.line-container {
  display: flex;
}
.dot-container {
  display: flex;
}
.dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin: 0 5px;
}
.blue-dot {
  background-color: #2c60d0;
  border: 2px solid white;
}
.red-dot {
  background-color: #f14249;
  border: 2px solid white;
}
.label {
  margin: 0 4px;
  font-size: 8px;
}
.left-label {
  order: -1;
}
.right-label {
  order: 1;
}
.bottom-label {
  margin-top: 4px;
  font-size: 8px;
}
</style>