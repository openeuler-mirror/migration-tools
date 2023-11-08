# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
from views import migration
try:
    from func import check
    agent_mods = {
        'check_storage': check.check_storage,
        'check_environment': check.check_environment,
        'check_os': check.check_os,
        'check_user': check.check_user,
        'check_repo': check.check_repo,
        'check_os_kernel': check.check_os_kernel,
        'check_repo_kernel': check.check_repo_kernel,
        'check_progress': check.check_progress,
        'export_migration_reports': check.export_reports,
        'system_migration': check.system_migration,
        'check_migration_progress': check.check_migration_progress,
        'migration_details': check.migration_details,
    }
except:
    pass


server_mods = {
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

