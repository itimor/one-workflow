<template>
  <div class="components-container">
    <aside>
      drag-list base on
      <a
        href="https://github.com/SortableJS/Vue.Draggable"
        target="_blank"
      >Vue.Draggable</a>
    </aside>
    <div class="editor-container">
      <dnd-list :list1="list1" :list2="list2" list1-title="List" list2-title="Article pool" />
    </div>
  </div>
</template>

<script>
import DndList from "@/components/DndList";

export default {
  name: "DndListDemo",
  components: { DndList },
  data() {
    return {
      all_list: [
        { id: 1, author: "admin", title: "111", content: "111", type: "CN" },
        { id: 2, author: "admin", title: "222", content: "222", type: "CN" },
        { id: 3, author: "admin", title: "333", content: "333", type: "CN" },
        { id: 4, author: "admin", title: "444", content: "444", type: "CN" },
        { id: 5, author: "admin", title: "555", content: "555", type: "CN" },
        { id: 6, author: "admin", title: "666", content: "666", type: "CN" }
      ],
      list1: [],
      list2: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.list1 = this.all_list.splice(0, 5);
      this.list2 = this.all_list;
    }
  }
};
</script>

