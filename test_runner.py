"""
test_runner.py - Automated Code Evaluation Engine
Safely evaluates user-submitted Python solutions against visible and hidden test cases,
captures stdout, measures execution time, and provides rich diagnostics.
"""

import io
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class ListNode:
    """Standard singly-linked list node for LeetCode style problems."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def list_to_linked_list(arr: Optional[List[Any]]) -> Optional[ListNode]:
    if not arr:
        return None
    dummy = ListNode(0)
    curr = dummy
    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next
    return dummy.next


def linked_list_to_list(head: Optional[ListNode]) -> List[Any]:
    result = []
    curr = head
    visited = set()
    while curr:
        if id(curr) in visited:
            result.append("...[CYCLE DETECTED]")
            break
        visited.add(id(curr))
        result.append(curr.val)
        curr = curr.next
    return result


class TreeNode:
    """Standard binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def list_to_tree(arr: Optional[List[Any]]) -> Optional[TreeNode]:
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        curr = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            curr.left = TreeNode(arr[i])
            queue.append(curr.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            curr.right = TreeNode(arr[i])
            queue.append(curr.right)
        i += 1
    return root


def tree_to_list(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        curr = queue.pop(0)
        if curr:
            result.append(curr.val)
            queue.append(curr.left)
            queue.append(curr.right)
        else:
            result.append(None)
    # Strip trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def normalize_for_comparison(val: Any, order_agnostic: bool = False) -> Any:
    """
    Normalizes complex structures for equality checking:
    Converts ListNodes and TreeNodes to serializable lists, and optionally sorts lists of lists.
    """
    if isinstance(val, ListNode):
        return linked_list_to_list(val)
    if isinstance(val, TreeNode):
        return tree_to_list(val)
    if isinstance(val, list):
        normalized = [normalize_for_comparison(x, order_agnostic) for x in val]
        if order_agnostic:
            try:
                # If elements are lists, sort each inner list, then sort the outer list
                sorted_inner = [sorted(x) if isinstance(x, list) else x for x in normalized]
                return sorted(sorted_inner, key=lambda x: str(x))
            except Exception:
                return normalized
        return normalized
    if isinstance(val, tuple):
        return list(val)
    return val


def values_are_equal(actual: Any, expected: Any, order_agnostic: bool = False) -> bool:
    """Compares actual output with expected output using normalized representations."""
    norm_actual = normalize_for_comparison(actual, order_agnostic)
    norm_expected = normalize_for_comparison(expected, order_agnostic)

    if norm_actual == norm_expected:
        return True

    # Float tolerance comparison
    if isinstance(norm_actual, (int, float)) and isinstance(norm_expected, (int, float)):
        return abs(norm_actual - norm_expected) < 1e-4

    return False


def execute_test_case(
    code: str,
    entry_point: str,
    problem_type: str,
    test_input: Any,
    expected_output: Any,
    order_agnostic: bool = False,
    timeout_sec: float = 3.0
) -> Dict[str, Any]:
    """
    Executes user code on a single test case within a timeout.
    Returns test outcome dictionary.
    """
    stdout_capture = io.StringIO()

    def run_worker():
        import collections
        import heapq
        import bisect
        import math
        import re
        import itertools

        # Setup standard context with interview modules
        global_scope = {
            "ListNode": ListNode,
            "TreeNode": TreeNode,
            "list_to_linked_list": list_to_linked_list,
            "linked_list_to_list": linked_list_to_list,
            "list_to_tree": list_to_tree,
            "tree_to_list": tree_to_list,
            "collections": collections,
            "deque": collections.deque,
            "Counter": collections.Counter,
            "defaultdict": collections.defaultdict,
            "heapq": heapq,
            "bisect": bisect,
            "math": math,
            "re": re,
            "itertools": itertools,
            "__builtins__": __builtins__,
        }

        old_stdout = sys.stdout
        sys.stdout = stdout_capture

        try:
            # Use global_scope as both globals and locals so top-level imports and functions share scope
            exec(code, global_scope)

            # Determine function or class
            target = global_scope.get(entry_point)
            if target is None:
                raise AttributeError(f"Target function or class '{entry_point}' not found in code submission.")

            # Problem execution patterns
            if problem_type == "function":
                # Standard function call with args
                args = test_input if isinstance(test_input, (list, tuple)) else [test_input]
                # Deep copy or transform inputs if needed
                transformed_args = []
                for a in args:
                    transformed_args.append(a)
                actual = target(*transformed_args)

            elif problem_type == "linked_list":
                # First arg or args need conversion from list to ListNode
                args = []
                if isinstance(test_input, list) and test_input and isinstance(test_input[0], list):
                    # Could be multiple lists
                    for a in test_input:
                        args.append(list_to_linked_list(a))
                elif isinstance(test_input, list):
                    args = [list_to_linked_list(test_input)]
                else:
                    args = [test_input]
                actual_node = target(*args)
                actual = linked_list_to_list(actual_node)

            elif problem_type == "merge_k_lists":
                # Special handler for Merge k Sorted Lists: test_input is list of lists
                inner = test_input[0] if (isinstance(test_input, list) and len(test_input) == 1 and isinstance(test_input[0], list)) else test_input
                list_nodes = [list_to_linked_list(l) for l in inner]
                actual_node = target(list_nodes)
                actual = linked_list_to_list(actual_node)

            elif problem_type == "tree":
                # Input is serialized tree list
                tree_arr = test_input[0] if (isinstance(test_input, list) and len(test_input) == 1 and isinstance(test_input[0], list)) else test_input
                root = list_to_tree(tree_arr)
                actual_res = target(root)
                if isinstance(actual_res, TreeNode):
                    actual = tree_to_list(actual_res)
                else:
                    actual = actual_res

            elif problem_type == "class_stream":
                # For MedianFinder or stateful class:
                # test_input is tuple: (commands_list, args_list)
                commands, arguments = test_input
                instance = None
                outputs = []
                for cmd, arg in zip(commands, arguments):
                    if cmd == entry_point:
                        instance = target(*arg)
                        outputs.append(None)
                    else:
                        method = getattr(instance, cmd)
                        res = method(*arg)
                        outputs.append(res)
                actual = outputs

            else:
                args = test_input if isinstance(test_input, (list, tuple)) else [test_input]
                actual = target(*args)

            return actual, None

        except Exception as e:
            tb = traceback.format_exc()
            return None, tb
        finally:
            sys.stdout = old_stdout

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_worker)
        try:
            actual_val, err_traceback = future.result(timeout=timeout_sec)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            captured_stdout = stdout_capture.getvalue()

            if err_traceback:
                return {
                    "passed": False,
                    "status": "ERROR",
                    "actual": None,
                    "expected": expected_output,
                    "error": err_traceback,
                    "stdout": captured_stdout,
                    "time_ms": round(elapsed_ms, 2),
                }

            passed = values_are_equal(actual_val, expected_output, order_agnostic=order_agnostic)
            return {
                "passed": passed,
                "status": "PASSED" if passed else "FAILED",
                "actual": normalize_for_comparison(actual_val),
                "expected": normalize_for_comparison(expected_output),
                "error": None,
                "stdout": captured_stdout,
                "time_ms": round(elapsed_ms, 2),
            }

        except FutureTimeoutError:
            return {
                "passed": False,
                "status": "TIMEOUT",
                "actual": None,
                "expected": expected_output,
                "error": f"Execution exceeded time limit of {timeout_sec}s. Watch out for infinite loops or high complexity!",
                "stdout": stdout_capture.getvalue(),
                "time_ms": timeout_sec * 1000.0,
            }


def run_all_tests(
    code: str,
    problem_meta: Dict[str, Any],
    only_visible: bool = False
) -> Dict[str, Any]:
    """
    Runs all test cases for a problem against user code.
    `only_visible=True` runs only sample test cases (for quick "Run Tests").
    `only_visible=False` runs the full test suite (for "Submit Solution").
    """
    tests = problem_meta.get("sample_tests", []) if only_visible else problem_meta.get("all_tests", [])
    entry_point = problem_meta.get("entry_point", "solve")
    problem_type = problem_meta.get("problem_type", "function")
    order_agnostic = problem_meta.get("order_agnostic", False)

    results = []
    all_passed = True
    total_time_ms = 0.0

    for i, t in enumerate(tests):
        test_input = t["input"]
        expected = t["expected"]
        res = execute_test_case(
            code=code,
            entry_point=entry_point,
            problem_type=problem_type,
            test_input=test_input,
            expected_output=expected,
            order_agnostic=order_agnostic,
            timeout_sec=problem_meta.get("timeout_sec", 3.0),
        )
        res["test_num"] = i + 1
        res["input_repr"] = str(t.get("display_input", test_input))
        res["is_hidden"] = t.get("hidden", False)
        total_time_ms += res["time_ms"]
        results.append(res)

        if not res["passed"]:
            all_passed = False

    passed_count = sum(1 for r in results if r["passed"])

    return {
        "all_passed": all_passed,
        "passed_count": passed_count,
        "total_count": len(results),
        "total_time_ms": round(total_time_ms, 2),
        "results": results,
    }
