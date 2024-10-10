<template>
  <div>
    <el-card class="box-card" style="margin: 10PX;width: 800px;"  v-loading="loading"
    element-loading-text="模型训练中"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)">
      <div style="margin-bottom: 10px;">训练集所占比例</div>
      <el-input v-model="proportion" placeholder="请输入占比"></el-input>
      <div style="margin-bottom: 10px;margin-top:20px">训练轮次</div>
      <el-input v-model="epochs" placeholder="请输入训练轮次"></el-input>

      <div style="margin-top: 50px;">选择数据集</div>
        <!--     文件     -->
      <div style="margin-top: 10px;">
          <el-upload
            :action="uploadUrl"
            :headers="uploadHeaders"
            :on-change="handleChange"
            :on-success="handleUploadSuccess"
            :on-exceed="handleUploadExceed"
            :file-list="fileList"
            :limit="1"
            accept=".csv"
          >
          <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </div>
        <el-button style="margin-top: 50px;" type="primary" @click="onSubmit">训练</el-button>
        <div style="margin-top: 20px;">输出：</div>
        <div style="width: 500px;height: 300px;margin-top: 8px;border: 1px solid #ddd;padding: 6px;">
          <div>正确率：{{ accuracy_score }}</div>
          <div style="margin-top:6px;">精度：{{precision_score}}</div>
          <div style="margin-top:6px;">召回率：{{ recall_score }}</div>
          <div style="margin-top:6px;">F1得分：{{ f1_score }}</div>
        </div>
    </el-card>
  </div>
 
</template>

<script>

import * as api from './api'
import util from '@/libs/util'

export default {
  name: 'Train',
  components: {
   
  },
  data () {
    return {
      proportion:'',
      epochs:1,
      uploadUrl: util.baseURL() + 'api/system/file/',
      uploadHeaders: {
        Authorization: 'JWT ' + util.cookies.get('token')
      },
      fileList:[],
      setting:{
        id:14,
        value:'',
        key:'models_params',
        title:'模型参数'
      },
      uploadFile:{
        id:'',
        name:'',
        size:'',
        url:''
      },
      loading:false,
      accuracy_score:'',
      precision_score:'',
      recall_score:'',
      f1_score:''
    }
  },
  methods: {
    handleUploadSuccess(response, file, fileList){
      console.log('file',file)
      console.log('response',response)
      const {id,name,size,url} = response.data
      this.uploadFile = {
        id,name,size,url
      }
    },
    handleChange(file, fileList) {
    },
    handleUploadExceed(files, fileList){
      this.$message.warning('最多只能上传一个文件，如果更新文件请先删除原文件')
    },
    onSubmit () {
      if(!this.uploadFile.id){
        this.$message.warning('请先上传数据集')
        return
      }
      const addForm = {proportion:this.proportion,...this.uploadFile}
      this.setting.value = JSON.stringify(addForm)
      api.UpdateObj(this.setting).then(res => {
            // this.$message.success('保存成功')
            this.loading = true
            this.train(this.proportion,this.uploadFile.url,this.epochs)
        })
    },
    train(proportion,url,epochs){
      api.Train(proportion,url,epochs).then(res => {
            // this.$message.success('保存成功')
            // this.loading = true
            console.log('@res',res)
            if(res.data){
              this.accuracy_score = res.data.accuracy_score
              this.precision_score = res.data.precision_score
              this.recall_score = res.data.recall_score
              this.f1_score = res.data.f1_score
            }
            this.loading = false
        }).catch(() => {
            this.loading = false
        })
    },
    getDetail(){
      api.GetDetailById(this.setting.id).then(res => {
          this.setting.value = res.data.value
          console.log('setting',this.setting)
          if(res.data.value){
            const jsonObj = JSON.parse(res.data.value);
            this.proportion = jsonObj.proportion;
            this.uploadFile = {
                id:jsonObj.id,
                name:jsonObj.name,
                size:jsonObj.size,
                url:jsonObj.url
            }
            this.fileList.push(this.uploadFile)
            // console.log('pagination',this.proportion)
          }
        })
    }
  },
  created () {
    this.getDetail()
  }
}
</script>

<style scoped>

</style>
