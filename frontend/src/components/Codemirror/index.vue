<template>
  <div class="code-editor">
    <textarea ref="textarea"></textarea>
  </div>
</template>

<script>
  import CodeMirror from 'codemirror'
  import 'codemirror/lib/codemirror.css'

  // language
  import 'codemirror/mode/python/python'
  import 'codemirror/mode/shell/shell'

  // theme css
  import 'codemirror/theme/monokai.css'
  // require active-line.js
  import 'codemirror/addon/selection/active-line.js'
  // styleSelectedText
  import 'codemirror/addon/selection/mark-selection.js'
  import 'codemirror/addon/search/searchcursor.js'
  // hint
  import 'codemirror/addon/hint/show-hint.js'
  import 'codemirror/addon/hint/show-hint.css'
  import 'codemirror/addon/hint/javascript-hint.js'
  import 'codemirror/addon/selection/active-line.js'
  // highlightSelectionMatches
  import 'codemirror/addon/scroll/annotatescrollbar.js'
  import 'codemirror/addon/search/matchesonscrollbar.js'
  import 'codemirror/addon/search/searchcursor.js'
  import 'codemirror/addon/search/match-highlighter.js'
  // keyMap
  import 'codemirror/mode/clike/clike.js'
  import 'codemirror/addon/edit/matchbrackets.js'
  import 'codemirror/addon/comment/comment.js'
  import 'codemirror/addon/dialog/dialog.js'
  import 'codemirror/addon/dialog/dialog.css'
  import 'codemirror/addon/search/searchcursor.js'
  import 'codemirror/addon/search/search.js'
  import 'codemirror/keymap/sublime.js'
  // foldGutter
  import 'codemirror/addon/fold/foldgutter.css'
  import 'codemirror/addon/fold/brace-fold.js'
  import 'codemirror/addon/fold/comment-fold.js'
  import 'codemirror/addon/fold/foldcode.js'
  import 'codemirror/addon/fold/foldgutter.js'
  import 'codemirror/addon/fold/indent-fold.js'
  import 'codemirror/addon/fold/markdown-fold.js'
  import 'codemirror/addon/fold/xml-fold.js'

  export default {
    name: 'codeEditor',
    /* eslint-disable vue/require-prop-types */
    props: {
      value: String
    },
    data() {
      return {
        editor: null
      }
    },
    watch: {
      value(newValue, preValue) {
        if (newValue !== preValue && newValue !== this.editor.getValue()) {
          this.editor.setValue(newValue)
        }
      }
    },
    mounted() {
      this.editor = CodeMirror.fromTextArea(this.$refs.textarea, {
        lineNumbers: true,
        mode: 'text/x-python',
        gutters: ['CodeMirror-lint-markers'],
        theme: 'monokai',
        lint: true
      })
      if (this.value) {
        this.editor.setValue(this.value)
      }
      this.editor.on('change', () => {
        this.$emit('input', this.editor.getValue())
      })
    },
    methods: {
      setValue(value) {
        console.log(value)
        this.editor.setValue(value)
      },
      getValue() {
        return this.editor.getValue()
      },
    }
  }
</script>

<style scoped>
  .code-editor {
    height: 100%;
    line-height: 24px;
    position: relative;
  }

  .code-editor >>> .CodeMirror {
    height: auto;
    min-height: 700px;
    max-height: 750px;
  }

  .code-editor >>> .CodeMirror-scroll {
    min-height: 700px;
    max-height: 750px;
  }

  .code-editor >>> .cm-s-rubyblue span.cm-string {
    color: #F08047;
  }
</style>
