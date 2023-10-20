<template>
  <div id="app" style="background-color: #ffffff">
  <h1 class="title">Content-based Controls for Music Large-scale Language Modeling</h1>
    <div class="author">
      Liwei Lin, Gus Xia, Junyan Jiang @<a href="http://www.musicxlab.com/">Music X Lab</a>
  </div>
  <div class="card">
    <div class="sub-sec">
        We equip <a href="https://arxiv.org/abs/2306.05284">MusicGen</a>, a text-to-music generation model, with direct and <b>content-based controls</b> on innate music languages,
        including chords, rhythms, and pianoroll.
        To achieve this, we contribute a Parameter-Efficient Fine-Tuning (PEFT) method tailored for
        Transformer-based audio language model fine-tuning. Our approach achieved
        low-resource semi-supervised learning, tuning with less than 4% parameters compared
        to the original model and training on a small dataset set with fewer than 300 <i>unannotated</i> songs.
        We illustrate the <b>chords</b> and <b>rhythms</b>  control power of the model. Moreover, by combining pianoroll and text descriptions,
        our system enables flexible music <b>style transfer</b> and <b>music variation generation</b>.
      <br>
      <br>
      See more details in our paper [coming soon] and try our model via github [coming soon] or huggingface [coming soon].

    </div>
  </div>
  <AudioGroup />
  </div>
</template>

<script>

import AudioGroup from "@/components/AudioGroup";
export default {
  name: 'App',

  components: {
    AudioGroup
  }
}
</script>

<style scoped>

.card{
  padding-top: 40px;
  margin-left: 5%;
  margin-right: 5%;
  font-family: "Google Sans",Arial,Helvetica,sans-serif;

}
.title{
  line-height: 2;
  color: #202124;
  font-size: 2em;
  font-weight: bolder;
  text-align: center;

}
.author{
  padding-top: 30px;
  text-align: center;
}

.sub-sec{
  /*border-bottom: 3px solid rgba(147, 147, 147, 0.5);*/

  line-height: 1.5;
  color: #202124;
  font-size: 1.1em;
  font-weight: normal;
  text-align: justify;
}
</style>