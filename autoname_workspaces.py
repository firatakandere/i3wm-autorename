import logging
import i3ipc

ICONS = {
    'firefox': '',
    'alacritty': '',
    'telegramdesktop': '',
    'spotify': '',
    'jetbrains-pycharm-ce': '',
    'discord': 'ﭮ',
    'code-oss': '﬏'
}

UNKNOWN_WINDOW_ICON = ''
EMPTY_WORKSPACE_ICON = ''


def get_window_icon(window_class):
    window_class = window_class.lower()

    if window_class in ICONS:
        return ICONS[window_class]

    logging.warning('No icon is found for window_class %s' % window_class)
    return UNKNOWN_WINDOW_ICON


def get_workspace_icon(workspace):
    if len(workspace.leaves()) == 0:
        return EMPTY_WORKSPACE_ICON
    else:
        return [get_window_icon(w.window_class) for w in workspace.leaves()]


def rename_workspaces(i3):
    for index, workspace in enumerate(i3.get_tree().workspaces()):
        icons = get_workspace_icon(workspace)

        new_title = str(workspace.num) + ': ' + '|'.join(icons)

        i3.command('rename workspace "%s" to "%s"' % (workspace.name, new_title))
        logging.info('renaming workspace "%s" to "%s"' % (workspace.name, new_title))


if __name__ == '__main__':
    i3 = i3ipc.Connection()

    rename_workspaces(i3)

    def event_handler(i3: i3ipc.Connection, e: i3ipc.events.IpcBaseEvent):
        if e.change in ['new', 'close', 'move']:
            rename_workspaces(i3)


    i3.on('window', event_handler)
    i3.on('workspace', event_handler)
    i3.main()
