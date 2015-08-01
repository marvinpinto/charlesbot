import charlesbot.plugins as m


def get_plugin_class(class_str, slack_client):
    """Convenience function to convert a string into a class name"""
    return getattr(m, class_str)(slack_client)


def initialize_plugins(slack_client, config_plugin_list_str):
    return_list = []
    if not config_plugin_list_str:
        return return_list
    p_list = config_plugin_list_str.split(',')
    for x in p_list:
        Pluginz = get_plugin_class(x, slack_client)
        return_list.append(Pluginz)
    return return_list
