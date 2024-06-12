<template>
  <el-main>
    <div>
      <h1>RPM 兼容性评估</h1>
      <p>
        该页面展示当前系统与 UnionTechOS 服务器版之间的 RPM 包兼容性评估结果和
        RPM 包的对比列表
      </p>
      <div id="headerInfo">
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">当前操作系统:</el-col>
          <el-col :span="18" style="margin-top: 5px">{{
            $root.data.rpmscan_tabs.current_os
          }}</el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle"
            >当前系统已装 RPM 数量:</el-col
          >
          <el-col :span="18" style="margin-top: 5px">{{
            rpmAnalyzeResult.length
          }}</el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">目标操作系统:</el-col>
          <el-col :span="18" style="margin-top: 5px">{{
            $root.data.rpmscan_tabs.target_os
          }}</el-col>
        </el-row>
        <el-row class="infoItemLineMargin" style="margin-top: 30px">
          <el-col :span="6" class="infoItemTitle">全部提供的包数:</el-col>
          <el-col :span="18"
            >{{ rpmAnalyzeEvaluate.allProvided }} 个，占比
            {{
              (
                (rpmAnalyzeEvaluate.allProvided / rpmAnalyzeResult.length) *
                100
              ).toFixed(2)
            }}%，其中含版本跳跃
            {{ rpmAnalyzeEvaluate.allProvidedWithVerLeaped }} 个</el-col
          >
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">部分提供的包数:</el-col>
          <el-col :span="18"
            >{{ rpmAnalyzeEvaluate.partiallyProvided }} 个，占比
            {{
              (
                (rpmAnalyzeEvaluate.partiallyProvided /
                  rpmAnalyzeResult.length) *
                100
              ).toFixed(2)
            }}%，其中含版本跳跃
            {{ rpmAnalyzeEvaluate.partiallyProvidedWithVerLeaped }} 个</el-col
          >
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">无提供的包数:</el-col>
          <el-col :span="18"
            >{{ rpmAnalyzeEvaluate.nothingProvided }} 个，占比
            {{
              (
                (rpmAnalyzeEvaluate.nothingProvided / rpmAnalyzeResult.length) *
                100
              ).toFixed(2)
            }}%</el-col
          >
        </el-row>
      </div>
    </div>
    <div style="margin-top: 60px">
      <div class="toolBarBox">
        <div class="left">
          <h2>RPM 列表</h2>
        </div>
        <div class="right">
          <el-popover placement="top" :width="165" trigger="hover">
            <p>在此选择标签以过滤结果</p>
            <div>
              <div class="tagCheckboxContainer">
                <el-checkbox
                  v-model="tagCheckBox.strictFilter"
                  class="left"
                  @change="tagCheckboxClicked()"
                ></el-checkbox>
                <div class="tagOptionItem">精确匹配标签</div>
              </div>
              <div class="tagCheckboxContainer">
                <el-checkbox
                  v-model="tagCheckBox.allProvided"
                  class="left"
                  @change="tagCheckboxClicked()"
                ></el-checkbox>
                <div class="pkgTagItem pkgTagItemAllProvided right">
                  All provided
                </div>
              </div>
              <div class="tagCheckboxContainer">
                <el-checkbox
                  v-model="tagCheckBox.particallyProvided"
                  class="left"
                  @change="tagCheckboxClicked()"
                ></el-checkbox>
                <div class="pkgTagItem pkgTagItemPartialProvided">
                  Partially provided
                </div>
              </div>
              <div class="tagCheckboxContainer">
                <el-checkbox
                  v-model="tagCheckBox.nothingProvided"
                  class="left"
                  @change="tagCheckboxClicked()"
                ></el-checkbox>
                <div class="pkgTagItem pkgTagItemNothingProvided">
                  Nothing provided
                </div>
              </div>
              <div class="tagCheckboxContainer">
                <el-checkbox
                  v-model="tagCheckBox.versionLeaped"
                  class="left"
                  @change="tagCheckboxClicked()"
                ></el-checkbox>
                <div class="pkgTagItem pkgTagItemVersionLeaped">
                  Version leaped
                </div>
              </div>
            </div>
            <template #reference>
              <el-button style="margin-right: 10px">过滤</el-button>
            </template>
          </el-popover>
          <el-input
            v-model="rpmKeyword"
            placeholder="按包名搜索 RPM 包（区分大小写）"
            style="width: 400px"
            @input="searchRPM()"
          />
        </div>
      </div>
      <el-collapse @change="handleChange">
        <el-collapse-item
          v-for="rpm in displayArray.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
          )"
          :key="rpm.pn"
          :title="rpm.pn"
          @click="onCollapseItemClicked(displayArray.indexOf(rpm))"
        >
          <template #title>
            <!-- 这玩意似乎就是【槽】， 可以用一个 template 代替上面那个 【:title】 -->
            <div class="collapseTitle">
              <div class="pkgName">{{ rpm.pn }}</div>
              <div class="pkgTags">
                <div
                  v-for="tag in rpm.tags"
                  :key="tag"
                  class="pkgTagItem"
                  :class="{
                    pkgTagItemAllProvided: tag == 'All provided',
                    pkgTagItemPartialProvided: tag == 'Partially provided',
                    pkgTagItemNothingProvided: tag == 'Nothing provided',
                    pkgTagItemVersionLeaped: tag == 'Version leaped',
                  }"
                >
                  {{ tag }}
                </div>
              </div>
            </div>
          </template>
          <div style="width: 100%" v-if="rpm.expand && !rpm.infScroll">
            <div>
              <el-row class="provideColumnTitle">
                <el-col :span="6">当前系统上该包的 Provides</el-col>
                <el-col :span="3" style="text-align: center">版本</el-col>
                <el-col :span="3" style="text-align: center"
                  >UnionTechOS 是否提供</el-col
                >
                <el-col :span="3" style="text-align: center">版本</el-col>
                <el-col :span="8">UnionTechOS 上提供该 Provides 的包名</el-col>
              </el-row>
            </div>
            <div class="line"></div>
            <div>
              <el-row
                v-for="provideMap in rpm.ppm"
                :key="provideMap"
                class="provideItem"
                :class="{ provideItemNoProvide: provideMap.upp.p == null }"
              >
                <el-col :span="6">{{ provideMap.op.p }}</el-col>
                <el-col :span="3" style="text-align: center">{{
                  provideMap.op.v
                }}</el-col>
                <el-col :span="3" style="text-align: center">{{
                  provideMap.upp.p ? "是" : "否"
                }}</el-col>
                <el-col :span="3" style="text-align: center">{{
                  provideMap.upp.v
                }}</el-col>
                <el-col :span="8">{{ provideMap.upn }}</el-col>
              </el-row>
            </div>
          </div>
          <div style="width: 100%" v-if="rpm.expand && rpm.infScroll">
            <div>
              <el-row class="provideColumnTitle">
                <el-col :span="6">当前系统上该包的 Provides</el-col>
                <el-col :span="3" style="text-align: center">版本</el-col>
                <el-col :span="3" style="text-align: center"
                  >UnionTechOS 是否提供</el-col
                >
                <el-col :span="3" style="text-align: center">版本</el-col>
                <el-col :span="8">UnionTechOS 上提供该 Provides 的包名</el-col>
              </el-row>
            </div>
            <div class="line"></div>
            <div class="infinite-list" style="overflow: auto">
              <el-row
                v-for="provideMap in rpm.showingPPM"
                :key="provideMap"
                class="provideItem"
                :class="{ provideItemNoProvide: provideMap.upp.p == null }"
              >
                <el-col :span="6">{{ provideMap.op.p }}</el-col>
                <el-col :span="3" style="text-align: center">{{
                  provideMap.op.v
                }}</el-col>
                <el-col :span="3" style="text-align: center">{{
                  provideMap.upp.p ? "Yes" : "No"
                }}</el-col>
                <el-col :span="3" style="text-align: center">{{
                  provideMap.upp.v
                }}</el-col>
                <el-col :span="8">{{ provideMap.upn }}</el-col>
              </el-row>
              <el-button
                type="primary"
                class="loadMoreButton"
                @click="loadShowingPPM(displayArray.indexOf(rpm))"
                v-if="!rpm.showingPPM.isAllLoaded"
                >点击加载更多</el-button
              >
              <el-button
                type="primary"
                disabled="true"
                class="loadMoreButton"
                v-if="rpm.showingPPM.isAllLoaded"
                >已全部加载</el-button
              >
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <div style="margin-top: 30px">
      <el-pagination
        v-model:current-page="currentPage"
        :page-sizes="[10, 15, 30, 50, 100]"
        :page-size="pageSize"
        :pager-count="16"
        @current-change="currentPageChange"
        @size-change="handleSizeChange"
        layout="total, sizes, prev, pager, next"
        :total="displayArray.length"
      >
      </el-pagination>
    </div>
  </el-main>
</template>

<script>
import { ref } from "vue";

export default {
  name: "RpmScan",
  props: {},
  setup() {
    console.log("setup");
    const handleChange = (val) => {
      console.log(val);
    };
    const currentPageChange = (val) => {
      console.log(val);
      window.scrollTo(0, 460); // TODO: 换成动态计算的
    };

    return {
      rpmKeyword: ref(""),
      handleChange,
      currentPageChange,
    };
  },
  /**
   * 当前这个文件，是一个 【Vue 组件】， 组件中的 data() 函数会在每个组件构建时被调用
   * （可以理解为构造函数的一部分，至少是可以实现【构造】的功能）
   */
  data() {
    return {
      rpmAnalyzeResult: [],
      displayArray: [],
      rpmAnalyzeEvaluate: {},
      currentPage: 1,
      pageSize: 10,
      tagCheckBox: {
        allProvided: false,
        particallyProvided: false,
        nothingProvided: false,
        versionLeaped: false,
        strictFilter: false,
      },
    };
  },
  created() {
    console.log("info:  ");
    console.log("created");
    this.rpmAnalyzeEvaluate = {
      allPkgCount: 0,
      allProvided: 0,
      partiallyProvided: 0,
      nothingProvided: 0,
      verLeaped: 0,
      allProvidedWithVerLeaped: 0,
      partiallyProvidedWithVerLeaped: 0,
    };

    this.rpmAnalyzeResult = this.$root.data.rpmscan_tabs.data;
    for (let i = 0; i < this.rpmAnalyzeResult.length; i++) {
      /**
       * tag 识别采用类似 Unix 权限值类似的方法
       * all = 1
       * partically = 2
       * nothing = 4
       * version leap = 8
       * 给每个记录都挂上这么个玩意，做 tag 过滤的时候直接比值就可以了
       */
      this.rpmAnalyzeResult[i].expand = false;
      this.rpmAnalyzeResult[i].tagSum = 0;
      if (this.rpmAnalyzeResult[i].tags.indexOf("All provided") != -1) {
        this.rpmAnalyzeResult[i].tagSum += 1;
        this.rpmAnalyzeEvaluate.allProvided++;
      }
      if (this.rpmAnalyzeResult[i].tags.indexOf("Partially provided") != -1) {
        this.rpmAnalyzeResult[i].tagSum += 2;
        this.rpmAnalyzeEvaluate.partiallyProvided++;
      }
      if (this.rpmAnalyzeResult[i].tags.indexOf("Nothing provided") != -1) {
        this.rpmAnalyzeResult[i].tagSum += 4;
        this.rpmAnalyzeEvaluate.nothingProvided++;
      }
      if (this.rpmAnalyzeResult[i].tags.indexOf("Version leaped") != -1) {
        this.rpmAnalyzeResult[i].tagSum += 8;
        this.rpmAnalyzeEvaluate.verLeaped++;
        if (this.rpmAnalyzeResult[i].tags.indexOf("All provided") != -1) {
          this.rpmAnalyzeEvaluate.allProvidedWithVerLeaped++;
        }
        if (this.rpmAnalyzeResult[i].tags.indexOf("Partially provided") != -1) {
          this.rpmAnalyzeEvaluate.partiallyProvidedWithVerLeaped++;
        }
      }
    }
    this.rpmAnalyzeEvaluate.allPkgCount = this.rpmAnalyzeResult.length;
    this.displayArray = this.rpmAnalyzeResult;
    console.log(this.rpmAnalyzeEvaluate);
  },
  mounted() {
    console.log("mounted");
  },
  methods: {
    // 在该模块内的自定义函数都应该放在 methods 里面。访问模块属性用 this
    loadJSON: function (json) {
      return new Promise((resolve, reject) => {
        try {
          return resolve(JSON.parse(json));
        } catch (e) {
          return reject(e);
        }
      });
    },

    searchRPM: function () {
      if (this.rpmKeyword.length == 0) {
        this.displayArray = this.rpmAnalyzeResult;
        this.filterWithTag();
        return;
      }
      this.displayArray = [];
      for (let i = 0; i < this.rpmAnalyzeResult.length; i++) {
        if (this.rpmAnalyzeResult[i].pn.indexOf(this.rpmKeyword) != -1) {
          this.displayArray.push(this.rpmAnalyzeResult[i]);
        }
      }
      this.filterWithTag();
    },

    onCollapseItemClicked: function (index) {
      let ppmMinLength = 20;

      if (this.displayArray[index].expand) {
        return;
      }

      if (this.displayArray[index].ppm.length <= ppmMinLength) {
        this.displayArray[index].expand = true;
      } else {
        this.displayArray[index].isAllLoaded = false;
        this.displayArray[index].expand = true;
        this.displayArray[index].infScroll = true;
        this.displayArray[index].showingPPM = []; // 增加这样一个数组，专门用于保存显示出来的 PPM
        for (let i = 0; i < ppmMinLength; i++) {
          this.displayArray[index].showingPPM[i] =
            this.displayArray[index].ppm[i];
        }
      }
    },

    handleSizeChange: function (size) {
      this.pageSize = size;
    },

    loadShowingPPM: function (currentPPMIndex) {
      let leapLength = 500; // 步长，每次会增加多少
      let totalPPMLength = this.displayArray[currentPPMIndex].ppm.length;
      let currentPPMLength =
        this.displayArray[currentPPMIndex].showingPPM.length;
      console.log(currentPPMLength);
      for (
        let i = currentPPMLength;
        i < currentPPMLength + leapLength && i < totalPPMLength;
        i++
      ) {
        this.displayArray[currentPPMIndex].showingPPM[i] =
          this.displayArray[currentPPMIndex].ppm[i];
        if (i == totalPPMLength - 1)
          this.displayArray[currentPPMIndex].showingPPM.isAllLoaded = true;
      }
    },

    loadShowingPPMModified: function () {
      console.log("should load");
    },

    tagCheckboxClicked: function () {
      if (this.rpmKeyword.length == 0) {
        this.displayArray = this.rpmAnalyzeResult;
        this.filterWithTag();
        return;
      }
      this.displayArray = [];
      for (let i = 0; i < this.rpmAnalyzeResult.length; i++) {
        if (this.rpmAnalyzeResult[i].pn.indexOf(this.rpmKeyword) != -1) {
          this.displayArray.push(this.rpmAnalyzeResult[i]);
        }
      }
      this.filterWithTag();
    },

    filterWithTag: function () {
      let tagSum = 0;
      if (this.tagCheckBox.allProvided) tagSum += 1;
      if (this.tagCheckBox.particallyProvided) tagSum += 2;
      if (this.tagCheckBox.nothingProvided) tagSum += 4;
      if (this.tagCheckBox.versionLeaped) tagSum += 8;

      if (tagSum == 0) {
        return;
      }

      let displayArrayLength = this.displayArray.length;
      let originDisplayArray = [];
      originDisplayArray = this.displayArray;

      this.displayArray = [];
      for (let i = 0; i < displayArrayLength; i++) {
        if (this.tagCheckBox.strictFilter) {
          // 严格模式，必须全匹配
          if (originDisplayArray[i].tagSum == tagSum) {
            this.displayArray.push(originDisplayArray[i]);
          }
        } else {
          if (originDisplayArray[i].tagSum == tagSum) {
            // 处理标签完全匹配
            this.displayArray.push(originDisplayArray[i]);
          } else if (tagSum == 1 && originDisplayArray[i].tagSum == 9) {
            // 选了 all ，把带 verleap 的也加上
            this.displayArray.push(originDisplayArray[i]);
          } else if (tagSum == 2 && originDisplayArray[i].tagSum == 10) {
            // 选了 part ，把带 verleap 的也加上
            this.displayArray.push(originDisplayArray[i]);
          } else if (tagSum == 8 && originDisplayArray[i].tagSum > 8) {
            this.displayArray.push(originDisplayArray[i]);
          }
        }
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-main {
  min-height: calc(100vh - 120px);
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.collapseTitle {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.pkgName {
  color: #606266;
  vertical-align: center;
  float: left;
  font-weight: bold;
}
.pkgTags {
  vertical-align: center;
  float: right;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.pkgTagItem {
  padding: 0px 5px 0px 5px;
  height: fit-content;
  line-height: 25px;
  border-radius: 4px;
  border-width: 1px;
  width: 120px;
  float: right;
  text-align: center;
  margin-right: 10px;
  margin-left: 10px;
  color: #606266;
  border-style: solid;
  font-family: "Helvetica";
}
.tagOptionItem {
  padding: 0px 5px 0px 5px;
  height: fit-content;
  line-height: 25px;
  width: 120px;
  float: right;
  text-align: center;
  margin-right: 10px;
  margin-left: 10px;
  color: #606266;
  font-family: "Helvetica";
}
.pkgTagItemAllProvided {
  border-color: #ccff99;
  background: #ccff99;
}
.pkgTagItemPartialProvided {
  border-color: #ffcc66;
  background: #ffcc66;
}
.pkgTagItemNothingProvided {
  border-color: #ff9999;
  background: #ff9999;
  color: white;
}
.pkgTagItemVersionLeaped {
  border-color: #ffff99;
  background: #ffff99;
}
.infoItemLineMargin {
  margin-top: 10px;
}
.infoItemTitle {
  color: #606266;
}
.line {
  width: 99%;
  height: 0;
  border-top: 1px solid var(--el-border-color-base);
}
.toolBarBox {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.left {
  vertical-align: center;
  float: left;
}
.right {
  vertical-align: center;
  float: right;
}
.provideColumnTitle {
  margin: 3px 10px 0px 2px;
  padding: 0px 4px 0px 2px;
}
.provideItem {
  margin: 3px 10px 0px 2px;
  padding: 0px 4px 0px 2px;
}
.provideItem:hover {
  margin: 3px 10px 0px 4px;
  padding: 0px 4px 0px 4px;
  border-radius: 3px;
  background: #ffffff;
  box-shadow: 2px 2px 4px #c2c2c2, -2px -2px 4px #f0eeee;
}
.provideItemNoProvide {
  color: rgb(75, 75, 75);
  background: #ffcccc;
  border-radius: 3px;
  margin: 3px 10px 0px 2px;
  padding: 0px 4px 0px 2px;
}
.provideItemNoProvide:hover {
  color: rgb(75, 75, 75);
  margin: 3px 10px 0px 4px;
  padding: 0px 4px 0px 4px;
  border-radius: 3px;
  background: #ffcccc;
  box-shadow: 2px 2px 4px #ffd6d6, -2px -2px 4px #fff1f1;
}
.infinite-list {
  height: 600px;
  padding: 0;
  margin: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
}
.loadMoreButton {
  height: 30px;
  margin: 10px 10px 10px 4px;
}
.tagCheckboxContainer {
  margin-bottom: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>
