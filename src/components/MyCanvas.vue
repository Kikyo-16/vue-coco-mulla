

<template>
    <div style="position: relative;">
      <canvas ref="layer1" width="1600" height="200"
              @mousemove="mousemove"
              @mouseleave="mouseleave"
              @mousedown="mousedown"
              @mouseup="mouseup"
      style="position: absolute;width: 100%;height: 120px; z-index: 3;"></canvas>
      <canvas ref="layer2" width="1600" height="200"
              style="position: absolute;width: 100%;height: 120px;  z-index: 2;"></canvas>
      <canvas ref="layer3" width="1600" height="200"
              style="position: absolute;width: 100%;height: 120px;  z-index: 1;"></canvas>
  </div>
</template>

<script>

function getColor(root, remain){
  if(root === "C")
    return "rgba(255,0,0, 0.3)"
  else if(root === "C#")
    return "rgba(255,150,50,0.3)"
  else if(root === "D")
    return "rgba(255,145,0,0.3)"
  else if(root === "D#" || root === "Eb")
    return "rgba(255,242,0,0.3)"
  else if(root === "E")
    return "rgb(0,128,0,0.3)"
  else if(root === "F")
    return "rgba(0,255,217,0.3)"
  else if(root === "F#")
    return "rgba(0,178,255,0.3)"
  else if(root === "G")
    return "rgba(0,0,128,0.3)"
  else if(root === "G#")
    return "rgba(34,0,255,0.3)"
  else if(root === "A")
    return "rgba(94,0,255,0.3)"
  else if(root === "A#" || root === "Bb")
    return "rgba(153,0,255,0.3)"
  else if(root === "B#")
    return "rgba(247,0,255,0.3)"
  return "rgba(220,220,220,0.3)"
}

function getTxtLen(txt){
  if(txt[1] === "N")
    return txt[0].length * 22;
  return txt[0].length * 22 + txt[1].length * 16;
}

function parseTime(t){
  let min = Math.floor(t);
  let sec =  Math.floor((t - min)*60);
  let min_s, sec_s;
  if(min < 10)
    min_s = "0" + min;
  else
    min_s = "" + min;

  if(sec < 10)
    sec_s = "0" + sec;
  else
    sec_s = "" + sec;

  return min_s + " : " + sec_s
}

export default {
  name: 'MyCanvas',
  props: {
    chords:{
      type: Object,
      require: true,
    },
    audioTag:{
      type: String,
      require: true,
    }
  },

  data(){

    return{
      chordCanvas: null,
      pgCanvas: null,
      ratio: 0,
      highlightBar: false,
      redBar: false,
      isDrag: false,
      init: false,
      globalInit: false,
      audio: this.audioTag,
      selectedTags: ["001/000", "001/000"]
    }
  },
  mounted() {
    let chordCanvas = this.$refs["layer2"];
    let pgCanvas = this.$refs["layer1"];
    let durCanvas = this.$refs["layer3"];
    this.chordCanvas = chordCanvas.getContext('2d');
    this.pgCanvas = pgCanvas.getContext('2d');
    this.durCanvas = durCanvas.getContext('2d');
    this.updateCanvas(this.selectedTags[0], this.selectedTags[1], 0., 0, 0, 0, 0);
  },
  methods:{

    updateCanvas(tag_sample, tag_ref, ratio, s, target, cur, dur){
      if(this.init){
        s = 0;
        this.init = false;
      }
      this.selectedTags = [tag_sample, tag_ref];
      this.audio = target;
      this.cur = cur;
      this.dur = dur;
      if(s === 0){
        this.clearPG();
        this.drawChords(tag_sample, tag_ref);
      }
      this.drawProgress(ratio, s);
      this.drawCurrentTime(cur, dur, ratio);
    },
    drawBackground(){

    },
    drawCurrentTime(current_t, duration, ratio){
      let width = this.$refs["layer3"].width;
      let height = this.$refs["layer3"].height;
      let ctx = this.durCanvas;
      let cur = parseTime(current_t);
      let dur = parseTime(duration);
      let x = ratio * width;
      let dt = 80
      ctx.clearRect(x - dt*2, height / 2 - 30, dt*4, 40);
      ctx.font = "22px Arial";
      ctx.fillStyle = "black";
      ctx.textAlign = "left top";
      ctx.fillText(cur, x - dt, height / 2 - 10, dt, 10);
      ctx.fillText(dur, x + 10, height / 2 - 10, dt, 10);

    },
    drawChords(tag_est, tag_ref){
      let width = this.$refs["layer2"].width;
      let height = this.$refs["layer2"].height;
      let ctx = this.chordCanvas;
      let data_est = this.chords[tag_est];
      let data_ref = this.chords[tag_ref];
      ctx.clearRect(0, 0, width, height);
      this.drawChordSegs(ctx, data_est, width, height, 0)
      this.drawChordSegs(ctx, data_ref, width, height, height/2.+.5)

    },

    drawChordSegs(ctx, data, width, height, y_offset){
      let offset = 0;
      let y_neg = 0;
      let st = 0;
      let w = width;

      for (let i = 0; i < data.length; ++ i){
        st = data[i][0] * width / 1001.;
        w = (data[i][1] - data[i][0]) * width / 1001.
        ctx.fillStyle = getColor(data[i][2], data[i][3]);
        ctx.fillRect(st, y_offset + 2, w, height/2.-4);
        ctx.fillStyle = "rgba(0, 0, 0, 0.2)";
        ctx.fillRect(st, y_offset+ 2, 5, height/2.-4);
        let txt = [data[i][2], data[i][3]];

        if(w > 10 && st + 2< offset){
          y_neg += 25;
          this.drawTags(ctx, st, y_offset + 25 + y_neg, width, height/2., txt);
        }else if(w > 10){
          y_neg = 0;
          this.drawTags(ctx, st, y_offset + 25 + y_neg, width, height/2., txt);
        }else{
          y_neg = 0;
        }
        if(w > 10){
          let slen = getTxtLen(txt);
          offset = w > slen ? st +w : st +slen;
        }
      }
    },

    drawTags(ctx, x, y, w, h, txt){
      ctx.font = "22px Comic Sans MS";
      ctx.fillStyle = "black";
      ctx.textAlign = "left top";
      ctx.fillText(txt[0], x + 8, y, w, h);
      if(txt[1]!== "N"){
        ctx.font = "16px Comic Sans MS";
        if(txt[0].length === 1)
          ctx.fillText(txt[1], x + 23, y, w, h);
        else
          ctx.fillText(txt[1], x + 40, y, w, h);
      }

    },
    clearPG(){
      let width = this.$refs["layer1"].width;
      let height = this.$refs["layer1"].height;
      let ctx = this.pgCanvas;
      ctx.clearRect(0, 0, width, height);
      ctx = this.durCanvas;
      ctx.clearRect(0, 0, width, height);

    },
    drawProgress(ratio, s){
      let width = this.$refs["layer1"].width;
      let height = this.$refs["layer1"].height;
      let ctx = this.pgCanvas;

      let dt = 16;

      if(s > 0){
        ctx.fillStyle = "rgba(0,0,0,0.06)";
        ctx.clearRect(width*ratio - dt, 0, dt*2, height);
        ctx.fillRect(width*ratio - dt - 2, 0, dt + 2, height);
      }else{
        ctx.fillStyle = "rgba(0,0,0,0.3)";
        ctx.fillRect(0, 0, width*ratio, height);
      }
      if(this.highlightBar){
        ctx.fillStyle = "rgba(255,0,0,0.8)";
        ctx.fillRect(width*ratio - 8, 0, 16, height);
        ctx.fillStyle = "rgba(255,255,255,0.8)";
        ctx.fillRect(width*ratio - 5, 0, 10, height);
        this.redBar = true;
      }else{
        this.redBar = false;
      }
      ctx.beginPath();
      ctx.strokeStyle = 'black';
      ctx.lineWidth = 4;
      ctx.moveTo(width*ratio, 0);
      ctx.lineTo(width*ratio, height);
      ctx.stroke();
      ctx.closePath();
      this.ratio = ratio;
    },
    isActive(e){
      return Math.abs(this.getMouseRatio(e) - this.ratio) < 0.2
    },
    getMouseRatio(e){
      let rect = this.$refs["layer1"].getBoundingClientRect();
      return (e.clientX - rect.left) / (rect.right - rect.left);
    },
    setBarStatus(s){
      if(s === 0){
        this.highlightBar = false;
        if(this.redBar)
          this.drawProgress(this.ratio, 1);
      }else{
        this.highlightBar = true;
        if(!this.redBar)
          this.drawProgress(this.ratio, 1);
      }
    },
    mouseleave(e){
      if(this.isDrag){
        //this.$emit('playAudio', [this.audio, this.ratio]);
      }
      this.isDrag = false;
      this.setBarStatus(0);
    },
    mousemove(e){
      if(this.isActive(e)){
        this.setBarStatus(1);
      }else{
        this.setBarStatus(0);
      }
      if(this.isDrag){
        let newRatio = this.getMouseRatio(e);
        this.updateCanvas(this.selectedTags[0], this.selectedTags[1], newRatio, 0, this.audio, newRatio*this.dur, this.dur);
      }
    },
    mousedown(e){
      if(this.highlightBar){
        if(!this.isDrag){
          this.$emit('pauseAudio', this.audio);
        }
        this.isDrag = true;
        this.init = true;
      }

    },
    mouseup(e){
      if(this.isDrag){
        this.$emit('playAudio', [this.audio, this.ratio]);
      }
      this.isDrag = false;
      //this.setBarStatus(0);
    },

  }

}
</script>
