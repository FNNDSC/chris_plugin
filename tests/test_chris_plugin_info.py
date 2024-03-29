from chris_plugin.tool.chris_plugin_info import strip_version


def test_strip_version():
    assert strip_version("chris_plugin") == "chris_plugin"
    assert strip_version("chris_plugin~=0.0.7") == "chris_plugin"
    assert strip_version("chris_plugin<=0.0.7") == "chris_plugin"
    assert strip_version("chris_plugin>=0.0.7") == "chris_plugin"
    assert strip_version("chris_plugin==0.0.7") == "chris_plugin"
    assert strip_version("chris_plugin>0.0.7") == "chris_plugin"
    assert strip_version("chris_plugin<0.0.7") == "chris_plugin"
    assert strip_version("chris_plugin (~=0.0.9)") == "chris_plugin"
