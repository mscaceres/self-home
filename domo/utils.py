def find_class(base_package_name, cls_name):
    # If some exception is raised I expect to not be catch and program to stop so we can fix it.
    base_package = importlib.import_module(base_package_name)
    cls = None
    for mdl_name in base_package.__all__:
        child_mdl = importlib.import_module("{}.{}".format(base_package_name, mdl_name))
        try:
            cls = getattr(child_mdl, cls_name)
        except AttributeError:
            # class not found in this module, try next one
            pass
        else:
            # found a class match in a module
            break
    if cls is None:
        mdls_path = ", ".join([base_package_name + "." + mdl for mdl in base_package.__all__])
        raise AttributeError("Class {} not found in {}".format(cls_name, mdls_path))
    else:
        return cls