#!/usr/bin/env python3


def decision(node, thresholds, left_childs, right_childs, features,
             returns, indentation=1):
    """
    TODO
    """
    cpp_code = ""
    # if no branching
    if thresholds[node] == -2:
        cpp_code += "{0}return {1};\n{2}}}\n".format("  "*indentation,
                                                     returns[node],
                                                     "  "*(indentation-1))
    else:
        cpp_code += "{0}if features[{1}] <= {2} {{\n".format("  "*indentation,
                                                             features[node],
                                                             thresholds[node])
        # if left child exists
        if left_childs[node] != -1:
            cpp_code += decision(left_childs[node], thresholds, left_childs,
                                 right_childs, features, returns,indentation+1)
        cpp_code += "{0}else {{\n".format("  "*indentation)
        # if right child exists
        if right_childs[node] != -1:
            cpp_code += decision(right_childs[node], thresholds, left_childs,
                                 right_childs, features, returns,indentation+1)
        cpp_code += "{0}}}\n".format("  "*(indentation-1))
    return cpp_code

def create_cpp_code(dt):
    """
    Translate sklearn decison tree model 'dt' into C++ code.
    Takes DecisionTreeClassifier or DecisionTreeRegressor as input.
    Returns 'DTPredict.hpp' header file.
    """
    count = dt.tree_.node_count
    features = dt.tree_.feature
    left_childs = dt.tree_.children_left
    right_childs = dt.tree_.children_right
    thresholds = dt.tree_.threshold
    returns = dt.tree_.value
    # feature_names = ["x{0}".format(i) for i in range(count)]
    # TODO: Add possibility to return target vector
    cpp_code = "inline double DTPredict(const std::vector<double> & features) {\n"
    cpp_code += decision(0, thresholds, left_childs, right_childs,
                         features, returns,1)
    print(cpp_code)

    # save code to .hpp file
    hpp_file = open("DTPredict.hpp","w+")
    hpp_file.write(cpp_code)
    hpp_file.close()