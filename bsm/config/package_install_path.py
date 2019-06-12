from bsm.config.common import Common

class PackageInstallPath(Common):
    def __init__(self, config_release, config_category, config_package_install):
        super(PackageInstallPath, self).__init__()

        category_priority = config_release.get('setting', {}).get('category_priority', [])
        category_install = [ctg for ctg in category_priority if config_category.get(ctg, {}).get('install')]
        category_install += [ctg for ctg, cfg in config_category.items() if ctg not in category_install and cfg.get('install')]

        for category in category_install:
            for subdir in config_package_install[category]:
                for package in config_package_install[category][subdir]:
                    for version, value in config_package_install[category][subdir][package].items():
                        if package in self:
                            continue
                        self[package] = value['config'].get('path', {}).copy()
