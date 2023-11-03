# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
from views import migration

mods = {
        'check_environment': migration.check_environment,
        'check_storage': migration.check_storage,
        'check_os': migration.check_os,
        'check_os_kernel': migration.check_os_kernel,
        'check_migration_progress': migration.check_migration_progress,
        'check_progress': migration.check_progress,
        'check_repo': migration.check_repo,
        'check_repo_kernel': migration.check_repo_kernel,
        'check_user': migration.check_user,
        'close_tool': migration.close_tool,
        'export_migration_reports': migration.export_migration_reports,
        'system_migration': migration.system_migration,
        'migration_details': migration.migration_details,
        }
