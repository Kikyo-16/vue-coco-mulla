<template>



  <div class="card">
    <div class="sub-sec">
    <h2 >
      Chord and Drums Condition
    </h2>
      Chord and rhythm controls via symbolic chord representation and acoustic drum tracks.
      <br>
      We transcribe chord progression of the generated audio samples using a <a href="https://github.com/music-x-lab/ISMIR2019-Large-Vocabulary-Chord-Recognition">chord recognition model</a>.
      </div>
      <div class="audio-bar">
        <div class="chord-col">
          <div class="chord-name"> Estimated Chords of the Generated Sample</div>
          <div class="chord-name"> Conditioned Chords</div>
        </div>
        <my-canvas class="canvas"
            ref="drumsCanvas" :chords=drums_chords audioTag="111"
                      @pauseAudio="pauseTarget"
                      @playAudio="playTarget"/>
      </div>
      <div class="audio-bar">
        <div class="sample-name"></div>
      <div class="desc-ref" ref="desc11">Conditioned Drums</div>
        <div class="desc" ref="desc12">lazy jazz composition features a captivating saxophone solo
          that effortlessly melds with piano chords,
          skillfully weaving its way through the melody with languid grace.
          Instruments: saxophone, piano, drums.</div>
        <div class="desc" ref="desc13">relax folk song with a flute solo and acoustic guitar chords. instrument: flute, guitar, drums</div>
        <div class="desc" ref="desc14">happy piano with a swing melody. instrument: piano, drums</div>
        <div class="desc" ref="desc15">A grand orchestral arrangement with thunderous percussion, epic brass fanfares, and soaring strings, creating a cinematic atmosphere fit for a heroic battle.</div>
      </div>

      <div v-for="i in 5" :key="i">
        <div class="audio-bar">
          <div class="sample-name" :ref="'sample1'+i">{{"Sample 00" + i}}</div>
          <my-audio class="audio-ref"
              :musicSrc="drumsSrc[i - 1][0]"
                  :audioTag="[1, i, 1]"
                  :ref="'1'+i+'1'"
                  @play="updateAttrs(1, i, 1)"
                  @timeupdate="updateCanvas"/>
          <my-audio class="audio"
              :musicSrc="drumsSrc[i - 1][j]"
                  :audioTag="[1, i, j+1]"
                  :ref="'1'+i+(j+1)"
                  v-for="j in 4" :key="'1'+i+(j+1)"
                  @play="updateAttrs(1, i, j+1)"
                  @timeupdate="updateCanvas"/>
          </div>
      </div>
  </div>

  <div class="card">
    <div class="sub-sec">
    <h2 >
      Piano Roll Guidance
    </h2>
      Content-based style transfer / music variation generation via chord and rhythm controls with symbolic piano roll hints.
      <br>
      The model incorporates musical elements from the provided piano roll, such as walking bass or motifs.
      </div>
    <div class="demo-desc">

    </div>
    <div class="audio-bar">
        <div class="chord-col">
          <div class="chord-name"> Estimated Chords of the Generated Sample</div>
          <div class="chord-name"> Conditioned Chords</div>
        </div>
      <my-canvas class="canvas"
          ref="pianoCanvas" :chords=piano_chords audioTag="211"
            @pauseAudio="pauseTarget"
            @playAudio="playTarget"/>
    </div>
    <div class="audio-bar">
        <div class="sample-name"></div>
      <div class="desc-ref" ref="desc21">Conditioned Drums and Piano Roll</div>
        <div class="desc" ref="desc22">lazy jazz composition features a captivating saxophone solo
          that effortlessly melds with piano chords,
          skillfully weaving its way through the melody with languid grace.
          Instruments: saxophone, piano, drums.</div>
        <div class="desc" ref="desc23">relax folk song with a flute solo and acoustic guitar chords. instrument: flute, guitar, drums</div>
        <div class="desc" ref="desc24">happy piano with a swing melody. instrument: piano, drums</div>
        <div class="desc" ref="desc25">A grand orchestral arrangement with thunderous percussion, epic brass fanfares, and soaring strings, creating a cinematic atmosphere fit for a heroic battle.</div>
      </div>
      <div v-for="i in 5" :key="i">
        <div class="audio-bar">
          <div class="sample-name"  :ref="'sample2'+i">{{"Sample 00" + i}}</div>
          <my-audio class="audio-ref"
              :musicSrc="pianoSrc[i - 1][0]"
                  :audioTag="[2, i, 1]"
                  :ref="'2'+i+'1'"
                  @play="updateAttrs(2, i, 1)"
                  @timeupdate="updateCanvas"/>
          <my-audio class="audio"
              :musicSrc="pianoSrc[i - 1][j]"
                  :audioTag="[2, i, j+1]"
                  :ref="'2'+i+(j+1)"
                  v-for="j in 4" :key="'1'+i+(j+1)"
                  @play="updateAttrs(2, i, j+1)"
                  @timeupdate="updateCanvas"/>
          </div>
      </div>

    </div>

</template>

<script>
import MyAudio from './MyAudio.vue'
import MyCanvas from './MyCanvas.vue'

function generate_file_list(i) {
  let prefix = "./audios/00" + i + "/00";
  let res = Array(0);
  for(let j = 1; j <=5; ++ j){
    let t_res = Array(0)
    for(let k=0; k <=5;++k){
      t_res.push(prefix + j+"/00"+k + ".wav")
    }
    res.push(t_res);
  }
  return res;
}

function generate_chords(tag){
  if(tag === "drums"){
    return require("../assets/drums_chords.json")[0];
  }else if(tag === "piano"){
    return require("../assets/piano_chords.json")[0];
  }else{
    return require("../assets/full_chords.json")[0];
  }
}

export default {
  name: 'AudioGroup',
  components: {
    MyAudio, MyCanvas
  },
  props: {
    drumsSrc: {
      type: Array,
      default: generate_file_list(1),
    },
    pianoSrc: {
      type: Array,
      default: generate_file_list(2),
    },
    fullSrc: {
      type: Array,
      default: generate_file_list(3),
    },
    drums_chords: {
      type: Object,
      default: generate_chords("drums"),
    },
    piano_chords: {
      type: Object,
      default: generate_chords("piano"),
    },
    full_chords: {
      type: Object,
      default: generate_chords("full"),
    },
  },
  methods:{
    updateAttrs(si, sj, sk){
      this.reviseDiv(si, sj, sk);
      let target = "" + si + sj +sk;
      let pgs = this.$refs[target][0].getProgress();
      this.reviseCanvas(pgs[0], si, sj, sk, 0, pgs[1], pgs[2]);
      for(let i = 1; i<=2; i++)
        for(let j = 1; j<=5; j++)
          for(let k = 1; k<=5; k++){
            let name = "" + i + j +k;
            if(name !== target) {
              this.$refs[name][0].pause();
            }
          }
    },
    reviseDiv(si, sj, sk){
      if(si === 1){
        this.$refs.drumsCanvas.globalInit = true

      }else if(si === 2){
        this.$refs.pianoCanvas.globalInit = true
      }

      this.$refs["desc"+si+sk].style.background = "rgba(255, 0, 0, 0.1)";
      this.$refs["sample"+si+sj][0].style.background = "rgba(255, 0, 0, 0.1)";
      for(let k = 1; k<=5; k++){
        if(k !== sk )
          this.$refs["desc"+si+k].style.background = "rgba(255, 0, 0, 0)";
      }
      for(let j = 1; j<=5; j++){
        if(j !== sj )
          this.$refs["sample"+si+j][0].style.background = "rgba(255, 0, 0, 0)";
      }
    },
    reviseCanvas(pg, si, sj, sk, s, cur, dur){
      let target = "" + si + sj +sk;
      let tag_sample = "00" + sj + "/00" + (sk - 1);
      let tag_ref = "00" + sj + "/000";
      if(si === 1){
        this.$refs.drumsCanvas.updateCanvas(tag_sample, tag_ref, pg, s, target, cur, dur)
      }else if(si === 2){
        this.$refs.pianoCanvas.updateCanvas(tag_sample, tag_ref, pg, s, target, cur, dur)
      }
    },
    updateCanvas(t, tags){
      if(typeof t[0] !== "number")
        return
      this.reviseCanvas(t[0], tags[0], tags[1], tags[2], 1, t[1], t[2]);
    },
    pauseTarget(e){
      if(this.$refs[e] === undefined)
        return
      this.$refs[e][0].pause();
    },
    playTarget(e){
      if(e[0] === undefined || this.$refs[e[0]] === undefined)
        return
      this.$refs[e[0]][0].continue(e[1]);
    },

  }
}
</script>

<style scoped>

.card{
  padding-bottom: 40px;
  padding-top: 40px;
  margin-left: 5%;
  margin-right: 5%;
}

.audio-bar{
  clear: left;
  border-top: 1px solid rgba(147, 147, 147, 0.2);
  border-bottom: 1px solid rgba(147, 147, 147, 0.2);
  padding-top: 0.5%;
  padding-bottom: 0.3%;
}
.sample-name{
  float: left;
  padding: 1.5%;
  width: 8%;

}
.audio{
  width: 15%;
  padding-right:1%;
}
.audio-ref{
  width: 15%;
  padding-right:6%;
}
.canvas{
  width: 86%;height: 120px;
}
.desc{
  padding: 1%;
  width: 14.5%;
  float: left;

}
.desc-ref{
  padding: 1%;
  width: 18%;
  float: left;

}
.chord-name{
  font-size: 13px;
  width: 100%;
  height: 50%;
  padding-top: 10%;
  text-align: center;
}
.chord-col{
  float: left;
  width: 8%;
  padding-right: 2%;
  height: 120px;
}
.roll-bar{
  clear: left;
  height: 200px;
  overflow:auto;
}
.demo-desc{

}
.sub-sec{
  border-bottom: 3px solid rgba(147, 147, 147, 0.5);
  margin-bottom: 50px;
  padding-bottom: 6px;
}
</style>
