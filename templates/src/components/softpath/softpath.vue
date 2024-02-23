<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>软件仓库路径</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      请根据一下提示设置软件仓库地址
    </el-card>

    <el-card class="card">
      <el-row class="card-3">设置软件仓库路径</el-row>
      <div class="center">
        <div class="center-1" v-show="conter1">
          <el-row class="row">
            <div class="dian"></div>
            x86_64</el-row
          >

          <el-row class="inputDeep center-1-1" v-show="conter11">
            <p>CentOS 7系列平台</p>
            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="x86_64_7"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="x86center7 = true" />

            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>

          <el-row class="inputDeep center-1-1" v-show="conter12">
            <p>CentOS 8系列平台</p>
            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="x86_64_8"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="x86center8 = true" />

            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect1">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success1">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail1">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>
        </div>

        <div class="center-2" v-show="conter2">
          <el-row class="row"
            ><div class="dian"></div>
            aarch_64</el-row
          >

          <el-row class="inputDeep center-1-1" v-show="conter21">
            <p>CentOS 7系列平台</p>

            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="aarch_64_7"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="aarchcenter7 = true" />

            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect2">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success2">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail2">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>

          <el-row class="inputDeep center-1-1" v-show="conter22">
            <p>CentOS 8系列平台</p>
            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="aarch_64_8"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="aarchcenter8 = true" />
            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect3">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success3">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail3">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>
        </div>
      </div>
      <el-row class="zi">
        <el-row class="zi-1">例如：</el-row>
        <el-row class="zi-1 zi-3">在线仓库</el-row>
        <el-row class="zi-1 zi-3">http://0.0.0.0/ios/AppStream</el-row>
        <el-row class="zi-1 zi-3">http://0.0.0.0/ios/BaseOS</el-row>
        <el-row class="zi-1 zi-3">http://0.0.0.0/ios/kernel-4.18</el-row>
        <el-row class="zi-1 zi-2 zi-3">请输入：http://0.0.0.0/ios</el-row>
      </el-row>

      <!-- 弹窗1 -->
      <el-dialog
        title="CentOS 7 系列平台-软件仓库路径"
        :visible.sync="x86center7"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="close7">关闭</el-button>
        </div>
      </el-dialog>

      <!-- 弹窗2 -->
      <el-dialog
        title="CentOS 8 系列平台-软件仓库路径"
        :visible.sync="x86center8"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="x86center8value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="close8">关闭</el-button>
        </div>
      </el-dialog>

      <!-- 弹窗3 -->
      <el-dialog
        title="CentOS 7 系列平台-软件仓库路径"
        :visible.sync="aarchcenter7"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="aarchcenter7value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="aarchclose7">关闭</el-button>
        </div>
      </el-dialog>

      <!-- 弹窗4 -->

      <el-dialog
        title="CentOS 8 系列平台-软件仓库路径"
        :visible.sync="aarchcenter8"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="aarchcenter8value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="aarchclose8">关闭</el-button>
        </div>
      </el-dialog>
    </el-card>

    <div class="footer">
      <div>
        <el-row>
          <el-button @click="err()">取消</el-button>

          <el-button
            :disabled="
              this.x86_64_7 != '' ||
              this.x86_64_8 != '' ||
              this.aarch_64_7 != '' ||
              this.aarch_64_8 != ''
                ? false
                : true
            "
            @click="go()"
            >下一步</el-button
          >
        </el-row>
      </div>
    </div>
  </div>
</template>



<style src="./index.css" scoped>

</style>
