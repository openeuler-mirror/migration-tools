import { createApp } from 'vue'

import installElementPlus from './plugins/element'

import RpmScanApp from './components/RpmScanApp.vue'
import ConfigScanApp from './components/ConfigScanApp.vue'
import HardwareScanApp from './components/HardwareScanApp.vue'

var mainApp;

// 直接在这里根据报告类型的值来选择要启动的 App，本质上还是整了仨 app
if(window.utmt_report_mode=="scanconfig") {
    mainApp = createApp(ConfigScanApp);
} else if(window.utmt_report_mode=="rpmscan") {
    window.sysinfo = window.ut_current_system_info;
    window.rpmAnalyzeResult = window.utmt_report_data;
    window.rpmAnalyzeEvaluate = {
        allPkgCount: 0,
        allProvided: 0,
        partiallyProvided: 0,
        nothingProvided: 0,
        verLeaped: 0,
        allProvidedWithVerLeaped: 0,
        partiallyProvidedWithVerLeaped: 0,
    };
    mainApp = createApp(RpmScanApp);
} else if(window.utmt_report_mode=="scanhardware") {
    mainApp = createApp(HardwareScanApp);
}

installElementPlus(mainApp);
mainApp.mount('#app');