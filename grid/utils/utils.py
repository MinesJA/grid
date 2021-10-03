def values_except(dict, except_keys):
    """Get all values except ones associated with keys.

    Args:
        dict (Dict): Key Value pairs
        except_key (Any): Key to avoid

    Returns:
        Sequence[values]: [description]
    """
    # return [s for (i, s) in sender.siblings.items()
    #         if i != env.return_id]
    return [v for k, v in dict.items() if k not in except_keys]
