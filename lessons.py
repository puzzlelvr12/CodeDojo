"""
lessons.py - Structured "Code School" Curriculum for CodeDojo
Provides deep-dive markdown lessons, Big-O complexity matrices, universal templates,
and common trap patterns for every major data structures and algorithms interview category.
"""

from typing import Any, Dict, List

LESSONS: List[Dict[str, Any]] = [
    {
        "id": "arrays_two_pointers",
        "title": "Arrays, Strings & Two Pointers",
        "icon": "🏹",
        "subtitle": "Pointer Invariants, In-Place Manipulation, and Memory Efficiency",
        "estimated_time": "25 mins",
        "related_problems": ["two_sum", "valid_palindrome", "best_time_to_buy_and_sell_stock", "three_sum"],
        "content": """
# 🏹 Arrays, Strings & Two Pointers Mastery

## 1. Core Philosophy & Mental Models
Arrays and strings form the bedrock of almost every technical interview. While brute force solutions frequently examine all $\\mathcal{O}(N^2)$ pairs or substrings, the **Two Pointer** technique leverages sorted properties or bidirectional scanning to compress time complexity down to $\\mathcal{O}(N)$ while maintaining $\\mathcal{O}(1)$ auxiliary space.

### The Three Archetypes of Two Pointers:
1. **Opposite Ends (Collision):** `left` starts at 0, `right` starts at $N-1$, moving inward until they meet. Ideal for sorted pair sums, palidromes, and boundary containment (e.g., Trapping Rain Water, Container With Most Water).
2. **Fast & Slow (Floyd's Cycle / In-Place Compaction):** Both start at the beginning, but one moves faster or conditionally. Ideal for removing duplicates in-place or detecting cycles.
3. **Prefix-Suffix Scans:** Scanning left-to-right then right-to-left to build aggregate knowledge without nested loops.

---

## 2. Big-O Complexity Matrix

| Operation / Pattern | Time Complexity | Auxiliary Space | Key Caveat |
| :--- | :--- | :--- | :--- |
| **Random Index Access** | $\\mathcal{O}(1)$ | $\\mathcal{O}(1)$ | Cache-friendly continuous memory block. |
| **Search in Unsorted Array** | $\\mathcal{O}(N)$ | $\\mathcal{O}(1)$ | Must inspect every cell in worst case. |
| **Search in Sorted Array** | $\\mathcal{O}(\\log N)$ | $\\mathcal{O}(1)$ | Binary search requires monotonic order. |
| **In-Place Two Pointer Scan** | $\\mathcal{O}(N)$ | $\\mathcal{O}(1)$ | Cannot maintain relative ordering if swapped indiscriminately. |
| **String Concatenation in Loop** | $\\mathcal{O}(N^2)$ | $\\mathcal{O}(N)$ | Strings are immutable in Python; creates new object every step! |
| **List Append (`.join()`)** | $\\mathcal{O}(N)$ | $\\mathcal{O}(N)$ | Always accumulate in list, then `''.join(chars)`. |

---

## 3. Battle-Tested Universal Templates

### Opposite-Ends Two Pointer Template
```python
def two_pointer_collision(arr: list[int]) -> int:
    left, right = 0, len(arr) - 1
    while left < right:
        # Evaluate current window / state
        current_val = arr[left] + arr[right]
        if current_val == target:
            return (left, right)
        elif current_val < target:
            left += 1   # Need larger sum in sorted array
        else:
            right -= 1  # Need smaller sum in sorted array
    return -1
```

### In-Place Compaction Template (Fast & Slow)
```python
def remove_duplicates_in_place(nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

---

## 4. The 5 Deadly Traps in Interviews

> [!WARNING]
> ### Trap 1: String Immutability Overhead
> In Python, doing `s += char` inside a loop creates an entirely new string of size $k$ on each iteration, ballooning an $\\mathcal{O}(N)$ algorithm into $\\mathcal{O}(N^2)$ time!
> **Antidote:** Append characters to a list `buf = []` and call `''.join(buf)` at the end.

> [!WARNING]
> ### Trap 2: Off-By-One Boundary Errors
> Does your loop run `while left < right` or `while left <= right`?
> - For pairs or collisions where $left$ and $right$ must be distinct elements: `while left < right:`.
> - For binary search where a single remaining element must be evaluated: `while left <= right:`.

> [!WARNING]
> ### Trap 3: Unhandled Duplicate Triplet Generation
> In problems like 3Sum, failing to skip identical adjacent elements leads to duplicate combinations in the result set or TLE when using a hash set.
> **Antidote:** Always skip duplicates immediately after advancing: `while left < right and nums[left] == nums[left+1]: left += 1`.
"""
    },
    {
        "id": "hash_maps_sets",
        "title": "Hash Maps & Sets Engine",
        "icon": "⚡",
        "subtitle": "Amortized O(1) Lookups, Frequency Frequency Analysis, and Space-Time Tradeoffs",
        "estimated_time": "20 mins",
        "related_problems": ["two_sum", "valid_anagram", "top_k_frequent_elements"],
        "content": """
# ⚡ Hash Maps & Sets Engine

## 1. Core Philosophy & Mental Models
The **Hash Map** is arguably the most powerful data structure in the technical interview arsenal. It trades $\\mathcal{O}(N)$ memory to turn $\\mathcal{O}(N)$ lookup scans into amortized $\\mathcal{O}(1)$ constant-time checks.

When encountering any problem asking for:
- "Find if a pair exists..."
- "Count the frequency of..."
- "Detect if any element repeats..."
- "Find the first unique element..."
Your immediate cognitive reflex should be: **Can a Hash Map store past knowledge as we iterate?**

---

## 2. Big-O Complexity Matrix

| Operation | Average Case | Worst Case | Worst Case Cause |
| :--- | :--- | :--- | :--- |
| **Lookup (`key in map`)** | $\\mathcal{O}(1)$ | $\\mathcal{O}(N)$ | Pathological hash collision degradation. |
| **Insertion (`map[key] = val`)** | $\\mathcal{O}(1)$ | $\\mathcal{O}(N)$ | Dynamic table resizing / re-hashing. |
| **Deletion (`del map[key]`)** | $\\mathcal{O}(1)$ | $\\mathcal{O}(N)$ | Collision bucket traversal. |
| **Iteration over Keys** | $\\mathcal{O}(K)$ | $\\mathcal{O}(K)$ | Proportional to number of unique keys $K$. |

---

## 3. Universal Python Patterns

### One-Pass Frequency Counter
```python
from collections import Counter, defaultdict

# Built-in Counter
counts = Counter(items)

# Or manual default dictionary for tracking indices
index_map = defaultdict(list)
for idx, val in enumerate(items):
    index_map[val].append(idx)
```

---

## 4. The 5 Deadly Traps in Interviews

> [!WARNING]
> ### Trap 1: Mutable Objects as Dictionary Keys
> Python dictionary keys MUST be hashable (immutable). You cannot use `list` or `set` as dictionary keys.
> **Antidote:** Cast lists or sets to `tuple(sorted(sublist))` or `frozenset` before indexing.

> [!WARNING]
> ### Trap 2: Modifying Dictionaries During Iteration
> Executing `for k in my_dict: del my_dict[k]` will raise a `RuntimeError: dictionary changed size during iteration`.
> **Antidote:** Iterate over a snapshot list: `for k in list(my_dict.keys()):`.
"""
    },
    {
        "id": "sliding_window",
        "title": "Sliding Window Paradigms",
        "icon": "🪟",
        "subtitle": "Monotonic Subarrays, Expansion/Contraction Invariants, and O(N) Bounds",
        "estimated_time": "25 mins",
        "related_problems": ["longest_substring_without_repeating", "minimum_window_substring"],
        "content": """
# 🪟 Sliding Window Paradigms

## 1. Core Philosophy & Mental Models
The **Sliding Window** technique is used on contiguous sequences (arrays or strings). Instead of recomputing properties of candidate substrings from scratch in $\\mathcal{O}(N^2)$ or $\\mathcal{O}(N^3)$, a sliding window maintains a dynamic state buffer:
- **Expand the Right Boundary:** Add elements into the window state one by one.
- **Contract the Left Boundary:** When the window violates a constraint (or when seeking minimal window), advance `left` to restore the invariant.

Every element enters the window once ($right$) and leaves at most once ($left$). Therefore, the overall time complexity is **strictly $\\mathcal{O}(N)$**, never $\\mathcal{O}(N^2)$!

---

## 2. Fixed vs Dynamic Windows

### A. Fixed Size Window (Length = $K$)
The window size is predetermined. Initialize the first $K$ elements, then for each subsequent index, subtract `arr[i - K]` and add `arr[i]`.

### B. Dynamic Window (Length = Variable)
Used when searching for the *longest* valid window or the *shortest* window satisfying a condition (e.g., Minimum Window Substring).

---

## 3. Universal Algorithmic Template

```python
def dynamic_sliding_window(s: str) -> int:
    left = 0
    window_state = {}
    best_result = 0

    for right in range(len(s)):
        # 1. Expand: include s[right] into window state
        char = s[right]
        window_state[char] = window_state.get(char, 0) + 1

        # 2. Contract: while window violates constraint
        while is_invalid(window_state):
            left_char = s[left]
            window_state[left_char] -= 1
            if window_state[left_char] == 0:
                del window_state[left_char]
            left += 1

        # 3. Update result with valid window
        best_result = max(best_result, right - left + 1)

    return best_result
```

---

## 4. The Deadly Traps

> [!WARNING]
> ### Trap: Negative Numbers in Subarray Sum Windows
> A classic interview trap: "Find the longest subarray with sum $\\le K$ when the array contains **negative** numbers."
> Sliding window **fails** here because adding an element does not monotonically increase the sum!
> **Antidote:** For arrays with negative numbers, use a **Prefix Sum + Hash Map** or Monotonic Queue instead of sliding window.
"""
    },
    {
        "id": "linked_lists",
        "title": "Linked Lists & Pointer Surgery",
        "icon": "🔗",
        "subtitle": "Dummy Heads, Floyd's Tortoise & Hare, and In-Place Pointer Reversals",
        "estimated_time": "25 mins",
        "related_problems": ["merge_k_sorted_lists"],
        "content": """
# 🔗 Linked Lists & Pointer Surgery

## 1. Core Philosophy & Mental Models
Linked lists test your ability to manipulate memory references safely without losing track of detached nodes. In an interview, a single misplaced pointer assignment causes orphaned chains, segmentation faults, or infinite cycle loops.

### The Two Golden Rules of Linked Lists:
1. **The Sentinel (Dummy) Node:** Always create a `dummy = ListNode(0)` whose `.next` points to `head`. Return `dummy.next`. This eliminates messy edge-cases where the head itself must be deleted or swapped.
2. **Cache Next Before Overwriting:** Before assigning `curr.next = prev`, always save the original destination: `nxt = curr.next`.

---

## 2. In-Place Reversal Blueprint

```python
def reverse_linked_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        nxt = curr.next   # 1. Save future reference
        curr.next = prev  # 2. Reverse pointer
        prev = curr       # 3. Step forward prev
        curr = nxt        # 4. Step forward curr
    return prev
```

---

## 3. Fast & Slow Pointer (Floyd's Cycle Algorithm)
- **Finding Middle Node:** Move `slow` by 1 step and `fast` by 2 steps. When `fast` reaches the end, `slow` is precisely at the midpoint!
- **Detecting Cycle:** If `slow == fast` ever becomes true, a cycle exists.
"""
    },
    {
        "id": "binary_search",
        "title": "Binary Search & Monotonic Predicates",
        "icon": "🎯",
        "subtitle": "Logarithmic Convergence, Rotated Spaces, and Searching on Solutions",
        "estimated_time": "25 mins",
        "related_problems": ["binary_search", "search_in_rotated_sorted_array", "max_profit_job_scheduling"],
        "content": """
# 🎯 Binary Search & Monotonic Predicates

## 1. Core Philosophy & Mental Models
Most candidates think Binary Search only applies to sorted arrays. Senior engineers know Binary Search applies to **any monotonic function** $f(x) \\rightarrow \\{0, 1\\}$.
If a condition transitions from `False, False, ..., True, True`, binary search can find the exact transition boundary in $\\mathcal{O}(\\log N)$ evaluations!

---

## 2. Universal Template (Closed Interval)

```python
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Overflow-safe
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## 3. Rotated Sorted Arrays Invariant
In a rotated sorted array (e.g., `[4, 5, 6, 7, 0, 1, 2]`), at least **one half is always normally sorted**.
Compare `nums[left]` with `nums[mid]`:
- If `nums[left] <= nums[mid]`, the left segment is strictly ascending.
- Otherwise, the right segment is strictly ascending.
"""
    },
    {
        "id": "trees_graphs",
        "title": "Trees, Graphs & Topological Sort",
        "icon": "🌲",
        "subtitle": "Breadth-First Search (BFS), Depth-First Search (DFS), and Directed Acyclic Graphs",
        "estimated_time": "30 mins",
        "related_problems": ["binary_tree_level_order_traversal", "word_ladder_ii", "alien_dictionary"],
        "content": """
# 🌲 Trees, Graphs & Topological Sort

## 1. Core Philosophy & Mental Models
Trees are simply restricted acyclic graphs with $N$ vertices and $N-1$ edges. When expanding to general graphs:
- **BFS (Queue / FIFO):** Guarantees the shortest path in unweighted graphs. Processes nodes layer-by-layer.
- **DFS (Recursion / Stack):** Explores deeply before backtracking. Ideal for pathfinding, topological sorting, and cycle detection.
- **Visited Tracking:** In cyclic graphs, forgetting a `visited = set()` causes an infinite loop!

---

## 2. Topological Sort (Kahn's BFS Algorithm)
Used whenever items have prerequisite dependencies (e.g., Course Schedule, Alien Dictionary, Build Systems).

### Kahn's Algorithm Blueprint:
1. Count `in_degree` (number of incoming prerequisite edges) for all vertices.
2. Enqueue all vertices with `in_degree == 0`.
3. While queue is not empty: pop vertex $u$, add to topological ordering, decrement `in_degree` of all outgoing neighbors $v$.
4. If a neighbor's `in_degree` drops to 0, enqueue it.
5. If processed count $< |V|$, a **cycle exists**!

```python
def topological_sort(num_nodes: int, edges: list[tuple]) -> list[int]:
    adj = collections.defaultdict(list)
    in_degree = [0] * num_nodes
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = collections.deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_nodes else [] # Empty if cycle
```
"""
    },
    {
        "id": "heaps_priority_queues",
        "title": "Heaps & Priority Queues",
        "icon": "⛰️",
        "subtitle": "Binary Heaps, Top-K Filtering, and Running Median Maintenance",
        "estimated_time": "20 mins",
        "related_problems": ["top_k_frequent_elements", "merge_k_sorted_lists", "median_from_data_stream"],
        "content": """
# ⛰️ Heaps & Priority Queues

## 1. Core Philosophy & Mental Models
A binary heap gives you $\\mathcal{O}(1)$ inspection of the minimum (or maximum) element while supporting $\\mathcal{O}(\\log N)$ insertions and deletions.

### When to deploy a Heap:
- Finding the $k$-th largest/smallest elements across large datasets.
- Merging multiple sorted streams in $\\mathcal{O}(N \\log K)$ time.
- Continuously computing running medians on dynamic streams.

---

## 2. Python's `heapq` Quirks
Python's `heapq` module is strictly a **Min-Heap**:
- To simulate a Max-Heap with numbers, invert signs: `heapq.heappush(heap, -x)`.
- When storing custom objects or tuples `(priority, object)`, Python compares subsequent elements in the tuple to break ties. If the object doesn't support `<` comparison, add an arbitrary unique counter: `(priority, counter, object)`.
"""
    },
    {
        "id": "dynamic_programming",
        "title": "Dynamic Programming (1D & 2D)",
        "icon": "🧩",
        "subtitle": "Optimal Substructure, Overlapping Subproblems, and Tabulation Transitions",
        "estimated_time": "30 mins",
        "related_problems": ["coin_change", "max_profit_job_scheduling"],
        "content": """
# 🧩 Dynamic Programming (1D & 2D)

## 1. Core Philosophy & Mental Models
Dynamic Programming is simply **recursion without redundant recalculation**. If a problem has:
1. **Optimal Substructure:** The optimal solution to the problem incorporates optimal solutions to smaller subproblems.
2. **Overlapping Subproblems:** The same subproblems are solved repeatedly if using naive recursion.

### The 4 Steps to Solve Any DP Problem:
1. **Define the State:** What does `dp[i]` or `dp[i][j]` represent in plain English? (e.g., `dp[x] = min coins to make amount x`).
2. **Identify the Transition:** Express `dp[i]` as a recurrence relation based on earlier states (e.g., `dp[x] = min(dp[x - c] + 1)`).
3. **Establish Base Cases:** What are the smallest non-decomposable states? (e.g., `dp[0] = 0`).
4. **Determine Direction of Computation:** Ensure dependencies are computed before states that rely on them.
"""
    },
    {
        "id": "boss_patterns",
        "title": "Boss-Level Hard Interview Killer Patterns",
        "icon": "👑",
        "subtitle": "Synthesizing Advanced Paradigms: Monotonic Stacks, Dual Balancing Heaps, and Bounded Backtracking",
        "estimated_time": "35 mins",
        "related_problems": ["trapping_rain_water", "merge_k_sorted_lists", "minimum_window_substring", "median_from_data_stream", "word_ladder_ii", "max_profit_job_scheduling", "alien_dictionary"],
        "content": """
# 👑 Boss-Level Hard Interview Killer Patterns

## 1. Deconstructing the "LeetCode Hard"
Top-tier interview questions (FAANG / Big Tech final rounds) rarely rely on a single trivial pattern. They require **synthesizing two orthogonal concepts** or enforcing strict invariant bounds under heavy constraints.

### The 7 Boss Archetypes:
1. **Volumetric Pooling Invariant (Trapping Rain Water):** Using two converging pointers with invariant bounds `left_max` and `right_max`.
2. **Multi-Way Stream Merging (Merge k Sorted Lists):** Priority queue with $(k)$ simultaneous pointers.
3. **Contractible Invariant Window (Minimum Window Substring):** Frequency maps with a separate `formed` counter for $\\mathcal{O}(1)$ valid tests.
4. **Dual Balancing Heaps (Median from Data Stream):** Splitting stream into a Max-Heap for the lower half and a Min-Heap for the upper half.
5. **Layered BFS + Backtracking (Word Ladder II):** Building a predecessor DAG with level-by-level BFS, then extracting all paths with reverse DFS.
6. **Disjoint Interval Scheduling (Maximum Profit in Job Scheduling):** Sorting intervals by end time, maintaining monotonic DP, and binary searching compatible non-overlapping predecessors with `bisect_right`.
7. **Topological Alphabet Inference (Alien Dictionary):** Constructing a directed graph from lexicographically ordered pairs and running Kahn's algorithm while guarding against prefix violations.
"""
    }
]


def get_all_lessons() -> List[Dict[str, Any]]:
    return LESSONS


def get_lesson_by_id(lesson_id: str) -> Dict[str, Any]:
    for l in LESSONS:
        if l["id"] == lesson_id:
            return l
    return LESSONS[0]
