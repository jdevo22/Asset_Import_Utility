<div align="center">
  <h1 align="center">Asset Import Utility</h1>
<!-- // Held for future use
  <img alt="Workflow status (with event)" src="https://img.shields.io/github/actions/workflow/status/jdevo22/Asset_Import_Utility/build.yml">
  <img alt="Release" src="https://img.shields.io/github/v/release/jdevo22/Asset_Import_Utility">
  <img alt="Total downloads" src="https://img.shields.io/github/downloads/jdevo22/Asset_Import_Utility/total">
  <img alt="Repo stars" src="https://img.shields.io/github/stars/jdevo22/Asset_Import_Utility">
  <img alt="Forks" src="https://img.shields.io/github/forks/jdevo22/Asset_Import_Utility">
  <img alt="Issues" src="https://img.shields.io/github/issues/jdevo22/Asset_Import_Utility">
  <img alt="Pull requests" src="https://img.shields.io/github/issues-pr/jdevo22/Asset_Import_Utility">
  <img alt="Project license" src="https://img.shields.io/github/license/jdevo22/Asset_Import_Utility">
 --> 
</div>

## Table of Contents

- [Latest Release](#latest-release)
- [Overview](#overview)
- [Supported Unity Versions](#supported-unity-versions)
- [Acknowledgements and Attributions](#acknowledgements-and-attributions)
  - [Trademarks](#trademarks)
  - [Assets](#assets)
- [License](#license)
- [Disclaimer](#disclaimer)

<!-- // Held for future use
- [Requirements](#requirements)
- [Usages](#usages)
  - [Android](#android)
  - [iOS](#ios)
- [Supported Platforms](#supported-platforms)

- [Contribute](#contribute)

- [FAQs](#faqs)
-->

## Latest Release

Version 1.1.0 changes how zip files are selected, switching from folder to individual file search. Folder search has been deprecated but will likely be re-implemented in a later release. 
The .blend file type has been disabled due to not being processed correctly and will be re-enabled once compatibility has been fixed.

## Overview

Simple Python script to unzip, rename, and move files into Unity projects.

This script extracts the specified zip files, renames textures files to the corresponding object, and moves all object files into an 'Imported Assets' folder and all texture files into a separate 'Textures' subfolder within the specified Unity project folder.

## Supported Unity Versions

This software interacts with the standard Unity project files and should be supported by all previous versions.

## Acknowledgements and Attributions

### Trademarks

This software is not sponsored by or affiliated with Unity Technologies or its affiliates. The Unity logo(s) are trademarks or registred trademarks of Unity Technologies or its affiliates in the U.S. and elsewhere.
<!-- // Unity logo guidelines
https://unity.com/legal/branding-trademarks
-->

### Assets

Zip file icon designed by Smashicons from [Flaticon](https://www.flaticon.com/free-icons/zip-format)

Box icon designed by Good Ware from [Flaticon](https://www.flaticon.com/free-icons/box)

## License

This project is licensed under GNU GPL 3.0.

For more information about the GNU General Public License version 3.0 (GNU GPL 3.0), please refer to the official GNU website: <https://www.gnu.org/licenses/gpl-3.0.html>

## Disclaimer

Please note that using this tool is at your own discretion and responsibility. Always make sure to backup your files before using any third-party tools or modifying assets.
