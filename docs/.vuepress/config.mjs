import { defineUserConfig } from "vuepress";
import { viteBundler } from "@vuepress/bundler-vite";
import { defaultTheme } from "@vuepress/theme-default";
import markdownItMultiMdTable from "markdown-it-multimd-table";

const sidebar = [
  {
    text: "Introduction",
    collapsible: false,
    children: ["/START.md", "/MODELS.md", "/FAQ.md"],
  },
  {
    text: "How to install",
    collapsible: false,
    children: ["/INSTALLER.md", "/BUILD.md", "/BOOT.md", "/POST-INSTALL.md"],
  },
  {
    text: "macOS Support",
    collapsible: false,
    children: ["/SEQUOIA-DROP.md", "/SONOMA-DROP.md", "/VENTURA-DROP.md", "/MONTEREY-DROP.md"],
  },
  {
    text: "Ongoing macOS issues",
    collapsible: false,
    children: ["/ONGOING-ISSUES.md"],
  },
  {
    text: "Application",
    collapsible: false,
    children: ["/UPDATE.md", "/UNINSTALL.md", "/PROCESS.md"],
  },
  {
    text: "Troubleshooting",
    collapsible: false,
    children: [
      "/TROUBLESHOOT-APP.md",
      "/TROUBLESHOOT-MISC.md",
      "/TROUBLESHOOT-NONMETAL.md",
      "/TROUBLESHOOT-HARDWARE.md",
      "/DEBUG.md",
    ],
  },
  {
    text: "Misc",
    collapsible: false,
    children: ["/TIMEMACHINE.md", "/ICNS.md", "/WINDOWS.md", "/UNIVERSALCONTROL.md"],
  },
  {
    text: "Credit",
    collapsible: false,
    children: ["/DONATE.md", "/LICENSE.md"],
  },
  {
    text: "Documentation",
    collapsible: false,
    children: ["/ISSUES-HOLD.md", "/TERMS.md", "/HOW.md", "/PATCHEXPLAIN.md"],
  },
];

export default defineUserConfig({
  title: "OpenCore Legacy Patcher",
  description: "Guide to put macOS on unsupported devices",
  base: "/OpenCore-Legacy-Patcher/",
  head: [
    ["meta", { name: "theme-color", content: "#3eaf7c" }],
    ["meta", { name: "apple-mobile-web-app-capable", content: "yes" }],
    ["meta", { name: "apple-mobile-web-app-status-bar-style", content: "black" }],
    ["link", { rel: "stylesheet", href: "/styles/website.css" }],
  ],
  bundler: viteBundler({
    viteOptions: {
      build: {
        cssMinify: false,
      },
    },
  }),
  theme: defaultTheme({
    logo: "/homepage.png",
    repo: "https://github.com/dortania/OpenCore-Legacy-Patcher/",
    docsDir: "docs",
    docsBranch: "main",
    editLink: true,
    editLinkText: "Help us improve this page!",
    lastUpdated: true,
    sidebar,
  }),
  markdown: {
    config: (md) => {
      md.use(markdownItMultiMdTable, {
        rowspan: true,
      });
    },
  },
  plugins: [],
});
