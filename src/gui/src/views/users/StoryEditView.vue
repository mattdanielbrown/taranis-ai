<template>
  <StoryEdit v-if="story" :story-prop="story" />
  <not-found-card v-else :item-id="storyId" item-type="Story" />
</template>

<script>
import StoryEdit from '@/components/assess/StoryEdit.vue'
import NotFoundCard from '@/components/common/NotFoundCard.vue'
import { computed, onBeforeMount } from 'vue'
import { useAssessStore } from '@/stores/AssessStore'
import { storeToRefs } from 'pinia'

export default {
  name: 'StoryEditView',
  components: {
    StoryEdit,
    NotFoundCard
  },
  props: {
    storyId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const assessStore = useAssessStore()
    const { storyByID } = storeToRefs(assessStore)
    const story = computed(() => storyByID.value(props.storyId))

    onBeforeMount(async () => {
      await assessStore.updateStoryByID(props.storyId)
    })

    return {
      story
    }
  }
}
</script>
