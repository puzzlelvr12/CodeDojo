"""
problems.py - Comprehensive Problem Bank for CodeDojo
Contains exhaustive interview challenges spanning Easy, Medium, and Boss Level (LeetCode Hard killers).
Each problem includes rich metadata, starter code, solutions, test cases, and multi-tier hints.
"""

from typing import Any, Dict, List

PROBLEMS: List[Dict[str, Any]] = [
    # =========================================================================
    # EASY / WARM-UPS
    # =========================================================================
    {
        "id": "two_sum",
        "title": "Two Sum",
        "boss_title": "Minion 1: The Binary Sentinels",
        "difficulty": "Easy",
        "category": "Arrays & Hash Maps",
        "xp": 100,
        "entry_point": "twoSum",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
Two sentinel guards stand at the gates of the cyber citadel. Each carries a numerical power crystal. To disable the forcefield, you must identify the **indices** of two crystals whose combined power equals the target lock frequency.

### 📜 Problem Statement
Given an array of integers `nums` and an integer `target`, return **indices of the two numbers** such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice. You can return the answer in any order.

### ⚡ Constraints
- $2 \\le \\text{len}(nums) \\le 10^4$
- $-10^9 \\le nums[i] \\le 10^9$
- $-10^9 \\le target \\le 10^9$
- Exactly one valid answer exists.
""",
        "starter_code": """def twoSum(nums: list[int], target: int) -> list[int]:
    # Write your solution here
    pass
""",
        "solution_code": """def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Hash Map Invariant
- **Time Complexity:** $\\mathcal{O}(N)$ — Single pass through the array.
- **Space Complexity:** $\\mathcal{O}(N)$ — Hash map storage for up to $N$ elements.

#### 💡 The Intuition
Instead of testing all pairs in $\\mathcal{O}(N^2)$ time with nested loops, leverage a hash map to trade spatial memory for instantaneous lookups. As we scan each number $x$, the required pair value is deterministically $complement = target - x$. If $complement$ was already indexed, we immediately return both indices.
""",
        "hints": {
            "nudge": "Can you remember the numbers you have previously seen in $\\mathcal{O}(1)$ time rather than looping through the array twice?",
            "blueprint": "Use a hash map (dictionary) where keys are the numbers and values are their corresponding indices. As you iterate through `nums`, calculate `target - num`. Check if that complement is in the map.",
            "master_scroll": "Initialize `seen = {}`. For each index `i` and number `num`, if `target - num` exists in `seen`, return `[seen[target - num], i]`. Otherwise, store `seen[num] = i`."
        },
        "sample_tests": [
            {"input": [[2, 7, 11, 15], 9], "expected": [0, 1], "display_input": "nums = [2, 7, 11, 15], target = 9"},
            {"input": [[3, 2, 4], 6], "expected": [1, 2], "display_input": "nums = [3, 2, 4], target = 6"},
        ],
        "all_tests": [
            {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"input": [[3, 2, 4], 6], "expected": [1, 2]},
            {"input": [[3, 3], 6], "expected": [0, 1]},
            {"input": [[-1, -2, -3, -4, -5], -8], "expected": [2, 4]},
            {"input": [[0, 4, 3, 0], 0], "expected": [0, 3]},
            {"input": [[1000000000, 500000000, 500000000], 1000000000], "expected": [1, 2]},
        ]
    },
    {
        "id": "valid_anagram",
        "title": "Valid Anagram",
        "boss_title": "Minion 2: The Cipher Decrypter",
        "difficulty": "Easy",
        "category": "Strings & Hash Maps",
        "xp": 100,
        "entry_point": "isAnagram",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
A scrambled rogue transmission has intercepted the Dojo frequencies. You must determine if signal string `t` is an exact permutation (anagram) of genuine handshake string `s`.

### 📜 Problem Statement
Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.
An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

### ⚡ Constraints
- $1 \\le \\text{len}(s), \\text{len}(t) \\le 5 \\times 10^4$
- `s` and `t` consist of lowercase English letters.
""",
        "starter_code": """def isAnagram(s: str, t: str) -> bool:
    # Write your solution here
    pass
""",
        "solution_code": """def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if ch not in counts or counts[ch] == 0:
            return False
        counts[ch] -= 1
    return True
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Frequency Counting
- **Time Complexity:** $\\mathcal{O}(N)$ — Linear scan over both strings of length $N$.
- **Space Complexity:** $\\mathcal{O}(1)$ — Up to 26 character keys in the frequency map for lowercase ASCII.

#### 💡 The Intuition
Strings of unequal length cannot be anagrams. Count character occurrences in `s`, then decrement counts when scanning `t`. If any character runs out or is missing, they are not anagrams.
""",
        "hints": {
            "nudge": "If two strings have different lengths, can they ever be anagrams? What data structure measures letter frequencies?",
            "blueprint": "Check lengths first. Then count the frequency of each character in `s` using a dictionary or array of size 26. Decrement for `t`. If all frequencies reach 0, return True.",
            "master_scroll": "Count frequencies with `counts = {}` for `s`. Loop through `t` and subtract. If any key drops below 0 or is absent, return `False`."
        },
        "sample_tests": [
            {"input": ["anagram", "nagaram"], "expected": True, "display_input": "s = 'anagram', t = 'nagaram'"},
            {"input": ["rat", "car"], "expected": False, "display_input": "s = 'rat', t = 'car'"},
        ],
        "all_tests": [
            {"input": ["anagram", "nagaram"], "expected": True},
            {"input": ["rat", "car"], "expected": False},
            {"input": ["a", "a"], "expected": True},
            {"input": ["ab", "a"], "expected": False},
            {"input": ["listen", "silent"], "expected": True},
            {"input": ["fluster", "restful"], "expected": True},
        ]
    },
    {
        "id": "valid_palindrome",
        "title": "Valid Palindrome",
        "boss_title": "Minion 3: The Mirror Monolith",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "xp": 100,
        "entry_point": "isPalindrome",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
The Mirror Monolith only unlocks when a passphrase reflects identically in forward and reverse telemetry, ignoring foreign symbols and casing.

### 📜 Problem Statement
A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string `s`, return `True` if it is a palindrome, or `False` otherwise.

### ⚡ Constraints
- $1 \\le \\text{len}(s) \\le 2 \\times 10^5$
- `s` consists only of printable ASCII characters.
""",
        "starter_code": """def isPalindrome(s: str) -> bool:
    # Write your solution here
    pass
""",
        "solution_code": """def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: In-Place Two Pointers
- **Time Complexity:** $\\mathcal{O}(N)$ — Each character evaluated at most twice.
- **Space Complexity:** $\\mathcal{O}(1)$ — Zero extra string allocations.

#### 💡 The Intuition
Using two pointers (`left` and `right`) starting at opposite ends avoids the memory overhead of creating a filtered duplicate string. Skip non-alphanumeric characters using `.isalnum()`, compare in lowercase, and advance inwards.
""",
        "hints": {
            "nudge": "Can you compare characters from both outer ends moving inward without allocating a new string?",
            "blueprint": "Use two pointers, `left = 0` and `right = len(s) - 1`. While `left < right`, advance past non-alphanumeric characters. Compare lowercased values. If unequal, return False.",
            "master_scroll": "Implement while `left < right`: skip with `not s[left].isalnum()`, skip `not s[right].isalnum()`. If `s[left].lower() != s[right].lower()`, return False. Else `left += 1; right -= 1`."
        },
        "sample_tests": [
            {"input": ["A man, a plan, a canal: Panama"], "expected": True, "display_input": "s = 'A man, a plan, a canal: Panama'"},
            {"input": ["race a car"], "expected": False, "display_input": "s = 'race a car'"},
        ],
        "all_tests": [
            {"input": ["A man, a plan, a canal: Panama"], "expected": True},
            {"input": ["race a car"], "expected": False},
            {"input": [" "], "expected": True},
            {"input": ["0P"], "expected": False},
            {"input": ["ab_a"], "expected": True},
            {"input": ["Was it a car or a cat I saw?"], "expected": True},
        ]
    },
    {
        "id": "best_time_to_buy_and_sell_stock",
        "title": "Best Time to Buy and Sell Stock",
        "boss_title": "Minion 4: The Market Speculator",
        "difficulty": "Easy",
        "category": "Arrays & Dynamic Programming",
        "xp": 100,
        "entry_point": "maxProfit",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
The Cyberpunk Stock Exchange fluctuates wildly. You must identify the single optimal day to purchase and the single subsequent day to sell a quantum asset to harvest maximum net credits.

### 📜 Problem Statement
You are given an array `prices` where `prices[i]` is the price of a given stock on the $i$-th day.
You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.
Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.

### ⚡ Constraints
- $1 \\le \\text{len}(prices) \\le 10^5$
- $0 \\le prices[i] \\le 10^4$
""",
        "starter_code": """def maxProfit(prices: list[int]) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """def maxProfit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: One-Pass Tracking
- **Time Complexity:** $\\mathcal{O}(N)$ — Single iteration through the price sequence.
- **Space Complexity:** $\\mathcal{O}(1)$ — Constant memory for two tracking variables.

#### 💡 The Intuition
At any given day $i$, the maximum profit if you sell on day $i$ is `prices[i] - minimum_price_seen_so_far`. Keep running track of the minimum buy price and maximum profit.
""",
        "hints": {
            "nudge": "If you sold on day $i$, what was the best day to have bought? Keep track of the lowest dip so far.",
            "blueprint": "Maintain `min_price = infinity` and `max_profit = 0`. For each price, update `min_price = min(min_price, price)` and `max_profit = max(max_profit, price - min_price)`.",
            "master_scroll": "Initialize `min_price = float('inf')` and `max_profit = 0`. Iterate through `prices`, updating both variables. Return `max_profit`."
        },
        "sample_tests": [
            {"input": [[7, 1, 5, 3, 6, 4]], "expected": 5, "display_input": "prices = [7, 1, 5, 3, 6, 4]"},
            {"input": [[7, 6, 4, 3, 1]], "expected": 0, "display_input": "prices = [7, 6, 4, 3, 1]"},
        ],
        "all_tests": [
            {"input": [[7, 1, 5, 3, 6, 4]], "expected": 5},
            {"input": [[7, 6, 4, 3, 1]], "expected": 0},
            {"input": [[1, 2]], "expected": 1},
            {"input": [[2, 4, 1]], "expected": 2},
            {"input": [[3, 3, 3, 3]], "expected": 0},
            {"input": [[1, 2, 4, 2, 5, 7, 2, 4, 9, 0]], "expected": 8},
        ]
    },
    {
        "id": "binary_search",
        "title": "Binary Search",
        "boss_title": "Minion 5: The Monotonic Scanner",
        "difficulty": "Easy",
        "category": "Binary Search",
        "xp": 100,
        "entry_point": "search",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
Search an ascending register of encrypted mainframe memory sectors in $\\mathcal{O}(\\log N)$ time. Any linear scan will trip the security alarms.

### 📜 Problem Statement
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.
You must write an algorithm with $\\mathcal{O}(\\log n)$ runtime complexity.

### ⚡ Constraints
- $1 \\le \\text{len}(nums) \\le 10^4$
- $-10^4 < nums[i], target < 10^4$
- All integers in `nums` are unique and sorted in ascending order.
""",
        "starter_code": """def search(nums: list[int], target: int) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Binary Search Invariants
- **Time Complexity:** $\\mathcal{O}(\\log N)$ — Search space halves on every comparison.
- **Space Complexity:** $\\mathcal{O}(1)$ — Constant pointers.

#### 💡 The Intuition
Maintain boundaries `[left, right]`. Compare the midpoint element with `target`. Because the array is strictly sorted, discard the half that cannot contain the target.
""",
        "hints": {
            "nudge": "How can you discard half the remaining numbers with a single comparison at each step?",
            "blueprint": "Use `left = 0`, `right = len(nums) - 1`. While `left <= right`, compute `mid = (left + right) // 2`. Narrow boundaries depending on whether `nums[mid]` is smaller or larger than `target`.",
            "master_scroll": "Loop `while left <= right`: calculate `mid = (left + right) // 2`. If `nums[mid] == target`, return `mid`. If `< target`, `left = mid + 1`, else `right = mid - 1`. Return `-1` if loop exits."
        },
        "sample_tests": [
            {"input": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4, "display_input": "nums = [-1, 0, 3, 5, 9, 12], target = 9"},
            {"input": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1, "display_input": "nums = [-1, 0, 3, 5, 9, 12], target = 2"},
        ],
        "all_tests": [
            {"input": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4},
            {"input": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1},
            {"input": [[5], 5], "expected": 0},
            {"input": [[5], -5], "expected": -1},
            {"input": [[1, 3, 5, 7, 9, 11, 13, 15], 1], "expected": 0},
            {"input": [[1, 3, 5, 7, 9, 11, 13, 15], 15], "expected": 7},
        ]
    },

    # =========================================================================
    # MEDIUM / CORE INTERVIEW PATTERNS
    # =========================================================================
    {
        "id": "longest_substring_without_repeating",
        "title": "Longest Substring Without Repeating Characters",
        "boss_title": "Sentinel 1: The Unique Buffer",
        "difficulty": "Medium",
        "category": "Sliding Window",
        "xp": 250,
        "entry_point": "lengthOfLongestSubstring",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
An encrypted data pipeline streams continuous character symbols. You must extract the length of the longest contiguous sub-buffer that contains no duplicate byte symbols.

### 📜 Problem Statement
Given a string `s`, find the length of the **longest substring** without repeating characters.

### ⚡ Constraints
- $0 \\le \\text{len}(s) \\le 5 \\times 10^4$
- `s` consists of English letters, digits, symbols and spaces.
""",
        "starter_code": """def lengthOfLongestSubstring(s: str) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """def lengthOfLongestSubstring(s: str) -> int:
    char_index_map = {}
    max_len = 0
    left = 0
    for right, ch in enumerate(s):
        if ch in char_index_map and char_index_map[ch] >= left:
            left = char_index_map[ch] + 1
        char_index_map[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Dynamic Sliding Window
- **Time Complexity:** $\\mathcal{O}(N)$ — Both pointers traverse the string in one pass.
- **Space Complexity:** $\\mathcal{O}(\\min(M, N))$ — Hash map stores the most recent index of each character.

#### 💡 The Intuition
Expand the window rightward. When a duplicate character is encountered that lies inside the current window (`char_index_map[ch] >= left`), jump the left boundary to `char_index_map[ch] + 1`. This skips all invalid prefix configurations in $\\mathcal{O}(1)$ time.
""",
        "hints": {
            "nudge": "When you encounter a duplicate character, can you jump the window's start pointer directly past the previous occurrence?",
            "blueprint": "Maintain a dictionary `char_index_map` tracking the last seen index of each character. For each character at `right`, if seen and its index is $\\ge left$, jump `left = char_index_map[ch] + 1`. Update `max_len = max(max_len, right - left + 1)`.",
            "master_scroll": "Initialize `char_index_map = {}`, `left = 0`, `max_len = 0`. Iterate `right, ch` in `enumerate(s)`. If `ch in char_index_map and char_index_map[ch] >= left`: update `left`. Record `char_index_map[ch] = right` and calculate window size."
        },
        "sample_tests": [
            {"input": ["abcabcbb"], "expected": 3, "display_input": "s = 'abcabcbb'"},
            {"input": ["bbbbb"], "expected": 1, "display_input": "s = 'bbbbb'"},
            {"input": ["pwwkew"], "expected": 3, "display_input": "s = 'pwwkew'"},
        ],
        "all_tests": [
            {"input": ["abcabcbb"], "expected": 3},
            {"input": ["bbbbb"], "expected": 1},
            {"input": ["pwwkew"], "expected": 3},
            {"input": [""], "expected": 0},
            {"input": [" "], "expected": 1},
            {"input": ["au"], "expected": 2},
            {"input": ["dvdf"], "expected": 3},
            {"input": ["tmmzuxt"], "expected": 5},
        ]
    },
    {
        "id": "three_sum",
        "title": "3Sum",
        "boss_title": "Sentinel 2: The Triad Alignment",
        "difficulty": "Medium",
        "category": "Two Pointers & Sorting",
        "xp": 250,
        "entry_point": "threeSum",
        "problem_type": "function",
        "order_agnostic": True,
        "description": """
### ⚔️ The Scenario
Three energy generators must synchronize their output frequencies so their sum perfectly cancels out to zero, preventing a reactor meltdown.

### 📜 Problem Statement
Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that $i \\ne j$, $i \\ne k$, and $j \\ne k$, and `nums[i] + nums[j] + nums[k] == 0`.
Notice that the solution set must not contain duplicate triplets.

### ⚡ Constraints
- $3 \\le \\text{len}(nums) \\le 3000$
- $-10^5 \\le nums[i] \\le 10^5$
""",
        "starter_code": """def threeSum(nums: list[int]) -> list[list[int]]:
    # Write your solution here
    pass
""",
        "solution_code": """def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
    return res
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Sort + Two Pointers
- **Time Complexity:** $\\mathcal{O}(N^2)$ — Sorting takes $\\mathcal{O}(N \\log N)$, and the two-pointer loop executes $N$ times.
- **Space Complexity:** $\\mathcal{O}(1)$ or $\\mathcal{O}(N)$ for sorting depending on Python's Timsort.

#### 💡 The Intuition
Sort `nums` first. Fix the first number `nums[i]`. Use two pointers `left` and `right` on the remainder of the array to find pairs summing to `-nums[i]`. Skip duplicates at all three pointer positions to guarantee uniqueness.
""",
        "hints": {
            "nudge": "If the array was sorted, could you reduce 3Sum into a series of Two-Pointer searches?",
            "blueprint": "Sort `nums`. Iterate index `i` from `0` to `n-3`. If `nums[i] == nums[i-1]`, skip to avoid duplicates. Then run two pointers `left = i + 1` and `right = n - 1`. If sum == 0, record triplet and skip subsequent duplicates for both pointers.",
            "master_scroll": "Sort `nums`. For `i` in range: skip duplicates. While `left < right`: if sum < 0, `left += 1`; if sum > 0, `right -= 1`; if sum == 0, append and advance past duplicate values for both `left` and `right`."
        },
        "sample_tests": [
            {"input": [[-1, 0, 1, 2, -1, -4]], "expected": [[-1, -1, 2], [-1, 0, 1]], "display_input": "nums = [-1, 0, 1, 2, -1, -4]"},
            {"input": [[0, 1, 1]], "expected": [], "display_input": "nums = [0, 1, 1]"},
            {"input": [[0, 0, 0]], "expected": [[0, 0, 0]], "display_input": "nums = [0, 0, 0]"},
        ],
        "all_tests": [
            {"input": [[-1, 0, 1, 2, -1, -4]], "expected": [[-1, -1, 2], [-1, 0, 1]]},
            {"input": [[0, 1, 1]], "expected": []},
            {"input": [[0, 0, 0]], "expected": [[0, 0, 0]]},
            {"input": [[-2, 0, 1, 1, 2]], "expected": [[-2, 0, 2], [-2, 1, 1]]},
            {"input": [[-1, 0, 1]], "expected": [[-1, 0, 1]]},
            {"input": [[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]], "expected": [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]},
        ]
    },
    {
        "id": "search_in_rotated_sorted_array",
        "title": "Search in Rotated Sorted Array",
        "boss_title": "Sentinel 3: The Fractured Axis",
        "difficulty": "Medium",
        "category": "Binary Search",
        "xp": 250,
        "entry_point": "search",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
The security rotor has rotated the memory address ring by an unknown pivot point. You must locate the target address in $\\mathcal{O}(\\log N)$ operations without unrolling the ring.

### 📜 Problem Statement
There is an integer array `nums` sorted in ascending order (with distinct values).
Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` ($1 \\le k < \\text{len}(nums)$) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.
You must write an algorithm with $\\mathcal{O}(\\log n)$ runtime complexity.

### ⚡ Constraints
- $1 \\le \\text{len}(nums) \\le 5000$
- $-10^4 \\le nums[i], target \\le 10^4$
- All values of `nums` are unique.
""",
        "starter_code": """def search(nums: list[int], target: int) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        # Check which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is normally sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is normally sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Partitioned Binary Search
- **Time Complexity:** $\\mathcal{O}(\\log N)$ — One half is always completely sorted.
- **Space Complexity:** $\\mathcal{O}(1)$ — Constant pointers.

#### 💡 The Intuition
Even when rotated, at least one half (either `[left..mid]` or `[mid..right]`) is guaranteed to be strictly sorted. Test whether `nums[left] <= nums[mid]`. If so, check if `target` lies within that sorted range. If yes, search left; otherwise search right. Mirror this logic if the right half is the sorted one.
""",
        "hints": {
            "nudge": "In a rotated sorted array, if you split it at `mid`, is at least one half guaranteed to be completely normally sorted?",
            "blueprint": "Find `mid`. Compare `nums[left]` and `nums[mid]`. If `nums[left] <= nums[mid]`, the left segment is sorted. Test if `target` is within `nums[left]` and `nums[mid]`. Otherwise, the right segment is sorted.",
            "master_scroll": "Implement binary search. If `nums[left] <= nums[mid]`, check if `nums[left] <= target < nums[mid]` to set `right = mid - 1`, else `left = mid + 1`. In the opposite case, check if `nums[mid] < target <= nums[right]` to set `left = mid + 1`, else `right = mid - 1`."
        },
        "sample_tests": [
            {"input": [[4, 5, 6, 7, 0, 1, 2], 0], "expected": 4, "display_input": "nums = [4, 5, 6, 7, 0, 1, 2], target = 0"},
            {"input": [[4, 5, 6, 7, 0, 1, 2], 3], "expected": -1, "display_input": "nums = [4, 5, 6, 7, 0, 1, 2], target = 3"},
            {"input": [[1], 0], "expected": -1, "display_input": "nums = [1], target = 0"},
        ],
        "all_tests": [
            {"input": [[4, 5, 6, 7, 0, 1, 2], 0], "expected": 4},
            {"input": [[4, 5, 6, 7, 0, 1, 2], 3], "expected": -1},
            {"input": [[1], 0], "expected": -1},
            {"input": [[1], 1], "expected": 0},
            {"input": [[5, 1, 3], 5], "expected": 0},
            {"input": [[5, 1, 3], 3], "expected": 2},
            {"input": [[4, 5, 6, 7, 8, 1, 2, 3], 8], "expected": 4},
        ]
    },
    {
        "id": "binary_tree_level_order_traversal",
        "title": "Binary Tree Level Order Traversal",
        "boss_title": "Sentinel 4: The Hierarchical Scanner",
        "difficulty": "Medium",
        "category": "Trees (BFS)",
        "xp": 250,
        "entry_point": "levelOrder",
        "problem_type": "tree",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
The AI consciousness hierarchy is organized as a binary tree of nodes. You must traverse each level horizontally from left to right, collecting telemetry data tier by tier.

### 📜 Problem Statement
Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).
Note: Tree nodes are represented using standard `TreeNode(val, left, right)` class.

### ⚡ Constraints
- The number of nodes in the tree is in the range $[0, 2000]$.
- $-1000 \\le Node.val \\le 1000$
""",
        "starter_code": """# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def levelOrder(root) -> list[list[int]]:
    # Write your solution here
    pass
""",
        "solution_code": """from collections import deque

def levelOrder(root) -> list[list[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)
    return result
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Queue-Based Breadth First Search (BFS)
- **Time Complexity:** $\\mathcal{O}(N)$ — Each node is enqueued and dequeued exactly once.
- **Space Complexity:** $\\mathcal{O}(W)$ where $W$ is the maximum width of the tree (up to $N/2$ for full binary tree).

#### 💡 The Intuition
Snapshot the length of `queue` at the start of each while-loop iteration. That length corresponds exactly to the number of nodes in the current horizontal level. Pop that exact number of nodes, append their children, and store the level's values.
""",
        "hints": {
            "nudge": "How can you tell how many nodes belong to the current horizontal level before processing their children?",
            "blueprint": "Use a `collections.deque`. Push `root`. While the queue is not empty, record `level_size = len(queue)`. Loop `level_size` times, pop nodes, and enqueue any non-null left and right children.",
            "master_scroll": "Initialize `queue = deque([root]) if root else []`. While `queue`: take `len(queue)`, pop from left, append to level list, push children. Append level list to result."
        },
        "sample_tests": [
            {"input": [[3, 9, 20, None, None, 15, 7]], "expected": [[3], [9, 20], [15, 7]], "display_input": "root = [3, 9, 20, None, None, 15, 7]"},
            {"input": [[1]], "expected": [[1]], "display_input": "root = [1]"},
            {"input": [[]], "expected": [], "display_input": "root = []"},
        ],
        "all_tests": [
            {"input": [[3, 9, 20, None, None, 15, 7]], "expected": [[3], [9, 20], [15, 7]]},
            {"input": [[1]], "expected": [[1]]},
            {"input": [[]], "expected": []},
            {"input": [[1, 2, 3, 4, 5, 6, 7]], "expected": [[1], [2, 3], [4, 5, 6, 7]]},
            {"input": [[1, 2, None, 3, None, 4]], "expected": [[1], [2], [3], [4]]},
        ]
    },
    {
        "id": "combination_sum",
        "title": "Combination Sum",
        "boss_title": "Sentinel 5: The Energy Synthesis",
        "difficulty": "Medium",
        "category": "Backtracking",
        "xp": 250,
        "entry_point": "combinationSum",
        "problem_type": "function",
        "order_agnostic": True,
        "description": """
### ⚔️ The Scenario
Synthesize an exact quantity of plasma energy using distinct elemental fuel rods. Any fuel rod may be duplicated indefinitely, but every unique recipe combination must be recorded.

### 📜 Problem Statement
Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in **any order**.

The **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

### ⚡ Constraints
- $1 \\le \\text{len}(candidates) \\le 30$
- $2 \\le candidates[i] \\le 40$
- All elements of `candidates` are **distinct**.
- $1 \\le target \\le 40$
""",
        "starter_code": """def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    # Write your solution here
    pass
""",
        "solution_code": """def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    res = []
    candidates.sort()

    def backtrack(remain: int, combo: list[int], start_idx: int):
        if remain == 0:
            res.append(list(combo))
            return
        for i in range(start_idx, len(candidates)):
            cand = candidates[i]
            if cand > remain:
                break
            combo.append(cand)
            backtrack(remain - cand, combo, i)
            combo.pop()

    backtrack(target, [], 0)
    return res
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: State-Pruned Backtracking
- **Time Complexity:** $\\mathcal{O}(2^T)$ where $T = target / \\min(candidates)$.
- **Space Complexity:** $\\mathcal{O}(T)$ recursion depth stack.

#### 💡 The Intuition
Sort candidates first. At each decision point, iterate from `start_idx` to allow reusing the current number while preventing reverse permutations (which creates duplicates like `[2, 3]` and `[3, 2]`). Prune immediately when `candidate > remain`.
""",
        "hints": {
            "nudge": "How do you avoid generating permutations like `[2, 3]` and `[3, 2]` as duplicate combinations?",
            "blueprint": "Sort `candidates`. In your recursive function `backtrack(remain, combo, start_idx)`, loop `i` from `start_idx` to end. If `candidates[i] > remain`, break immediately. Recurse passing `i` as the next `start_idx`.",
            "master_scroll": "Define `backtrack(remain, combo, start)`: if `remain == 0`, save `list(combo)`. For `i` in `range(start, len(c))`: if `c[i] > remain` break. `combo.append(c[i])`, recurse with `start=i`, then `combo.pop()`."
        },
        "sample_tests": [
            {"input": [[2, 3, 6, 7], 7], "expected": [[2, 2, 3], [7]], "display_input": "candidates = [2, 3, 6, 7], target = 7"},
            {"input": [[2, 3, 5], 8], "expected": [[2, 2, 2, 2], [2, 3, 3], [3, 5]], "display_input": "candidates = [2, 3, 5], target = 8"},
            {"input": [[2], 1], "expected": [], "display_input": "candidates = [2], target = 1"},
        ],
        "all_tests": [
            {"input": [[2, 3, 6, 7], 7], "expected": [[2, 2, 3], [7]]},
            {"input": [[2, 3, 5], 8], "expected": [[2, 2, 2, 2], [2, 3, 3], [3, 5]]},
            {"input": [[2], 1], "expected": []},
            {"input": [[3, 5, 8], 11], "expected": [[3, 3, 5], [3, 8]]},
            {"input": [[7, 3, 2], 18], "expected": [[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 3, 3], [2, 2, 2, 2, 3, 7], [2, 2, 2, 3, 3, 3, 3], [2, 2, 7, 7], [2, 3, 3, 3, 7], [3, 3, 3, 3, 3, 3]]},
        ]
    },
    {
        "id": "top_k_frequent_elements",
        "title": "Top K Frequent Elements",
        "boss_title": "Sentinel 6: The Signal Spectrum",
        "difficulty": "Medium",
        "category": "Heaps & Hash Maps",
        "xp": 250,
        "entry_point": "topKFrequent",
        "problem_type": "function",
        "order_agnostic": True,
        "description": """
### ⚔️ The Scenario
Analyze the electromagnetic signal spectrum and extract the $k$ most rampant transmitter IDs polluting the Dojo comms.

### 📜 Problem Statement
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in **any order**.
Your algorithm's time complexity must be better than $\\mathcal{O}(n \\log n)$, where $n$ is the array's size.

### ⚡ Constraints
- $1 \\le \\text{len}(nums) \\le 10^5$
- $-10^4 \\le nums[i] \\le 10^4$
- $k$ is in the range $[1, \\text{number of unique elements}]$.
- It is guaranteed that the answer is unique.
""",
        "starter_code": """def topKFrequent(nums: list[int], k: int) -> list[int]:
    # Write your solution here
    pass
""",
        "solution_code": """import heapq
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    # Min-heap of size k: (frequency, num)
    heap = []
    for num, count in counts.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for count, num in heap]
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Min-Heap of Size K or Bucket Sort
- **Time Complexity:** $\\mathcal{O}(N \\log K)$ with min-heap, or $\\mathcal{O}(N)$ with bucket sort.
- **Space Complexity:** $\\mathcal{O}(N)$ for hash map and heap.

#### 💡 The Intuition
Count frequencies in $\\mathcal{O}(N)$ time. Maintain a min-heap bounded at size $k$. By evicting the smallest frequency whenever the heap exceeds $k$, the heap is guaranteed to retain the $k$ largest frequencies upon completion.
""",
        "hints": {
            "nudge": "How can keeping a min-heap of size $k$ allow you to avoid sorting all unique numbers?",
            "blueprint": "Use `collections.Counter` to find frequency of every number. Push `(freq, num)` onto a min-heap. When the heap size exceeds $k$, pop the minimum. At the end, return the $k$ numbers remaining.",
            "master_scroll": "Use `counts = Counter(nums)`. For each `num, count` in `counts.items()`: `heapq.heappush(heap, (count, num))`. If `len(heap) > k`: `heapq.heappop(heap)`. Return `[num for _, num in heap]`."
        },
        "sample_tests": [
            {"input": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2], "display_input": "nums = [1, 1, 1, 2, 2, 3], k = 2"},
            {"input": [[1], 1], "expected": [1], "display_input": "nums = [1], k = 1"},
        ],
        "all_tests": [
            {"input": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2]},
            {"input": [[1], 1], "expected": [1]},
            {"input": [[4, 1, -1, 2, -1, 2, 3], 2], "expected": [-1, 2]},
            {"input": [[5, 5, 5, 5, 2, 2, 1], 1], "expected": [5]},
            {"input": [[1, 1, 1, 2, 2, 3, 3, 3, 3, 4], 2], "expected": [3, 1]},
        ]
    },
    {
        "id": "coin_change",
        "title": "Coin Change",
        "boss_title": "Sentinel 7: The Currency Matrix",
        "difficulty": "Medium",
        "category": "Dynamic Programming",
        "xp": 250,
        "entry_point": "coinChange",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### ⚔️ The Scenario
Reconfigure cyber tokens into an exact target balance using the minimum possible number of individual token denominations.

### 📜 Problem Statement
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.
Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.
You may assume that you have an infinite number of each kind of coin.

### ⚡ Constraints
- $1 \\le \\text{len}(coins) \\le 12$
- $1 \\le coins[i] \\le 2^{31} - 1$
- $0 \\le amount \\le 10^4$
""",
        "starter_code": """def coinChange(coins: list[int], amount: int) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            if dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
    return dp[amount] if dp[amount] != float('inf') else -1
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Bottom-Up 1D DP (Unbounded Knapsack)
- **Time Complexity:** $\\mathcal{O}(C \\times A)$ where $C = \\text{len}(coins)$ and $A = amount$.
- **Space Complexity:** $\\mathcal{O}(A)$ for the DP array.

#### 💡 The Intuition
Let `dp[x]` be the fewest coins required to produce sum `x`. Base case `dp[0] = 0`. For every coin, for every value from `coin` to `amount`, transition: `dp[x] = min(dp[x], dp[x - coin] + 1)`. If `dp[amount]` remains $\\infty$, return `-1`.
""",
        "hints": {
            "nudge": "Can you compute the minimum coins needed for all values from 0 up to `amount` incrementally?",
            "blueprint": "Initialize an array `dp = [float('inf')] * (amount + 1)` with `dp[0] = 0`. For each coin, iterate `x` from `coin` to `amount`, setting `dp[x] = min(dp[x], dp[x - coin] + 1)`.",
            "master_scroll": "Create `dp` array initialized to infinity. Set `dp[0] = 0`. Outer loop over `coins`, inner loop `x` from `coin` to `amount + 1`: update `dp[x] = min(dp[x], dp[x - coin] + 1)`. Return `dp[amount]` if not infinity else `-1`."
        },
        "sample_tests": [
            {"input": [[1, 2, 5], 11], "expected": 3, "display_input": "coins = [1, 2, 5], amount = 11"},
            {"input": [[2], 3], "expected": -1, "display_input": "coins = [2], amount = 3"},
            {"input": [[1], 0], "expected": 0, "display_input": "coins = [1], amount = 0"},
        ],
        "all_tests": [
            {"input": [[1, 2, 5], 11], "expected": 3},
            {"input": [[2], 3], "expected": -1},
            {"input": [[1], 0], "expected": 0},
            {"input": [[2, 5, 10, 1], 27], "expected": 4},
            {"input": [[186, 419, 83, 408], 6249], "expected": 20},
        ]
    },

    # =========================================================================
    # HARD / BOSS LEVEL (THE 7 LEETCODE HARD INTERVIEW KILLERS)
    # =========================================================================
    {
        "id": "trapping_rain_water",
        "title": "Trapping Rain Water",
        "boss_title": "BOSS 1: The Leviathan Rainmaker",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "trap",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### 👹 Boss Dossier: The Leviathan Rainmaker
*The skies over Sector 7 tear open as acid downpours cascade onto jagged neon spires. Only a master ninja who computes the volumetric pooling capacity across the skyline can prevent the lower grid from short-circuiting.*

### 📜 Problem Statement
Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

### ⚡ Constraints
- $n == \\text{len}(height)$
- $1 \\le n \\le 2 \\times 10^4$
- $0 \\le height[i] \\le 10^5$
""",
        "starter_code": """def trap(height: list[int]) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Two-Pointer Monotonic Invariant
- **Time Complexity:** $\\mathcal{O}(N)$ — Single pass inward with two pointers.
- **Space Complexity:** $\\mathcal{O}(1)$ — Optimal constant space.

#### 💡 The Intuition
The trapped water at index $i$ is governed strictly by $\\min(\\text{left\\_max}, \\text{right\\_max}) - height[i]$.
If `left_max < right_max`, we know with mathematical certainty that the water level at `left + 1` is bounded strictly by `left_max`, regardless of any taller walls further to the right! Hence, we can advance `left` and directly add `left_max - height[left]`. Symmetrically, if `right_max <= left_max`, advance `right`.
""",
        "hints": {
            "nudge": "At any position, how high can water rise? It is limited by the shorter of the maximum walls to its left and right.",
            "blueprint": "Use two pointers `left = 0` and `right = len(height) - 1`. Track `left_max` and `right_max`. If `left_max < right_max`, advance `left`, update `left_max`, and add `left_max - height[left]`. Else advance `right`, update `right_max`, and add `right_max - height[right]`.",
            "master_scroll": "Initialize `left, right = 0, len(height) - 1`. Maintain running `left_max, right_max = height[left], height[right]`. In while loop `left < right`: compare `left_max` and `right_max`, advance the smaller pointer, update its max, and accumulate difference."
        },
        "sample_tests": [
            {"input": [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], "expected": 6, "display_input": "height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]"},
            {"input": [[4, 2, 0, 3, 2, 5]], "expected": 9, "display_input": "height = [4, 2, 0, 3, 2, 5]"},
        ],
        "all_tests": [
            {"input": [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], "expected": 6},
            {"input": [[4, 2, 0, 3, 2, 5]], "expected": 9},
            {"input": [[1, 2]], "expected": 0},
            {"input": [[3, 0, 0, 2, 0, 4]], "expected": 10},
            {"input": [[5, 4, 1, 2]], "expected": 1},
            {"input": [[0, 0, 0, 0]], "expected": 0},
            {"input": [[5, 2, 1, 2, 1, 5]], "expected": 14},
        ]
    },
    {
        "id": "merge_k_sorted_lists",
        "title": "Merge k Sorted Lists",
        "boss_title": "BOSS 2: The Multi-Headed Hydra",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "mergeKLists",
        "problem_type": "merge_k_lists",
        "order_agnostic": False,
        "description": """
### 👹 Boss Dossier: The Multi-Headed Hydra
*The Hydra spawns $k$ distinct venom streams, each ordered by lethal potency. You must weave all streams into a single unified sorted conduit before the matrix is corroded.*

### 📜 Problem Statement
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

### ⚡ Constraints
- $k == \\text{len}(lists)$
- $0 \\le k \\le 10^4$
- $0 \\le \\text{len}(lists[i]) \\le 500$
- $-10^4 \\le lists[i][j] \\le 10^4$
- `lists[i]` is sorted in ascending order.
- The sum of `len(lists[i])` will not exceed $10^4$.
""",
        "starter_code": """# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

def mergeKLists(lists: list) -> any:
    # Write your solution here
    pass
""",
        "solution_code": """import heapq

def mergeKLists(lists: list):
    heap = []
    # Push the head of each non-empty list into min-heap with tiebreaker index
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    dummy = ListNode(0)
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Priority Queue (Min-Heap)
- **Time Complexity:** $\\mathcal{O}(N \\log k)$ where $N$ is total nodes across all lists and $k$ is the number of lists.
- **Space Complexity:** $\\mathcal{O}(k)$ heap holding at most 1 node per list.

#### 💡 The Intuition
Instead of comparing all $k$ heads in $\\mathcal{O}(k)$ time at each step, load the head of each list into a priority queue. Pop the minimum node in $\\mathcal{O}(\\log k)$, append it to the result list, and push its next successor if present.
""",
        "hints": {
            "nudge": "At any moment, you only need to choose the smallest node among the current heads of the $k$ lists. What data structure extracts the minimum in $\\mathcal{O}(\\log k)$?",
            "blueprint": "Use `heapq`. Push tuples `(node.val, list_index, node)` for all non-empty list heads. In a while loop, pop the smallest node, attach it to your merged list, and if `node.next` exists, push `(node.next.val, list_index, node.next)`.",
            "master_scroll": "Initialize heap. Add `(head.val, idx, head)` for valid heads. Create dummy node. While heap: `heappop`, link to tail, push `node.next` back into heap if exists. Return `dummy.next`."
        },
        "sample_tests": [
            {"input": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "expected": [1, 1, 2, 3, 4, 4, 5, 6], "display_input": "lists = [[1, 4, 5], [1, 3, 4], [2, 6]]"},
            {"input": [[]], "expected": [], "display_input": "lists = []"},
            {"input": [[[]]], "expected": [], "display_input": "lists = [[]]"},
        ],
        "all_tests": [
            {"input": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
            {"input": [[]], "expected": []},
            {"input": [[[]]], "expected": []},
            {"input": [[[2], [-1]]], "expected": [-1, 2]},
            {"input": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            {"input": [[[-10, -5, 0], [-8, 2, 5], [-3, 1, 4]]], "expected": [-10, -8, -5, -3, 0, 1, 2, 4, 5]},
        ]
    },
    {
        "id": "minimum_window_substring",
        "title": "Minimum Window Substring",
        "boss_title": "BOSS 3: The Quantum Sieve",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "minWindow",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### 👹 Boss Dossier: The Quantum Sieve
*An encrypted transmission stream `s` contains the key sequence symbols of `t`. Locate the tightest, most compact window substring containing all required characters to breach the mainframe.*

### 📜 Problem Statement
Given two strings `s` and `t` of lengths `m` and `n` respectively, return the **minimum window substring** of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `""`.
The testcases will be generated such that the answer is unique.

### ⚡ Constraints
- $m == \\text{len}(s)$
- $n == \\text{len}(t)$
- $1 \\le m, n \\le 10^5$
- `s` and `t` consist of uppercase and lowercase English letters.
""",
        "starter_code": """def minWindow(s: str, t: str) -> str:
    # Write your solution here
    pass
""",
        "solution_code": """from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not s or not t or len(s) < len(t):
        return ""

    target_counts = Counter(t)
    required_unique = len(target_counts)
    window_counts = {}

    formed = 0
    left = 0
    best_len = float('inf')
    best_range = (0, 0)

    for right, ch in enumerate(s):
        window_counts[ch] = window_counts.get(ch, 0) + 1
        if ch in target_counts and window_counts[ch] == target_counts[ch]:
            formed += 1

        # Contract window from left while valid
        while left <= right and formed == required_unique:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_range = (left, right)

            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                formed -= 1
            left += 1

    return "" if best_len == float('inf') else s[best_range[0]:best_range[1] + 1]
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Contractible Sliding Window with Invariant Counter
- **Time Complexity:** $\\mathcal{O}(M + N)$ — Each character is visited at most twice.
- **Space Complexity:** $\\mathcal{O}(M + N)$ for character frequency maps.

#### 💡 The Intuition
Track how many unique characters in `t` have reached their required target count via variable `formed`. Expand `right` until `formed == required_unique`. Then, contract `left` to minimize the window while keeping the invariant satisfied. Record the minimum window found.
""",
        "hints": {
            "nudge": "Instead of checking every letter count repeatedly, can you maintain a counter `formed` that tracks how many unique characters in `t` have their frequency requirements satisfied?",
            "blueprint": "Count `t` in `target_counts`. Expand `right` pointer over `s`. When a character's count matches `target_counts`, increment `formed`. When `formed == len(target_counts)`, shrink `left` while valid and record the minimal window.",
            "master_scroll": "Use two pointers. While expanding `right`, record letter in `window_counts`. When valid (`formed == required`), enter while loop: update `best_len`, decrement `window_counts[s[left]]`, adjust `formed`, and `left += 1`."
        },
        "sample_tests": [
            {"input": ["ADOBECODEBANC", "ABC"], "expected": "BANC", "display_input": "s = 'ADOBECODEBANC', t = 'ABC'"},
            {"input": ["a", "a"], "expected": "a", "display_input": "s = 'a', t = 'a'"},
            {"input": ["a", "aa"], "expected": "", "display_input": "s = 'a', t = 'aa'"},
        ],
        "all_tests": [
            {"input": ["ADOBECODEBANC", "ABC"], "expected": "BANC"},
            {"input": ["a", "a"], "expected": "a"},
            {"input": ["a", "aa"], "expected": ""},
            {"input": ["ab", "b"], "expected": "b"},
            {"input": ["cabwefgewcwaefgcf", "cae"], "expected": "cwae"},
            {"input": ["aaaaaaaaaaaabbbbbcdd", "abcdd"], "expected": "abbbbbcdd"},
        ]
    },
    {
        "id": "median_from_data_stream",
        "title": "Median from Data Stream",
        "boss_title": "BOSS 4: The Dynamic Gyroscope",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "MedianFinder",
        "problem_type": "class_stream",
        "order_agnostic": False,
        "description": """
### 👹 Boss Dossier: The Dynamic Gyroscope
*Real-time sensor numbers flood into the navigation system continuously. You must calculate the precise running median in $\\mathcal{O}(1)$ time while inserting incoming values in $\\mathcal{O}(\\log N)$ operations.*

### 📜 Problem Statement
The **median** is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

Implement the `MedianFinder` class:
- `MedianFinder()` initializes the `MedianFinder` object.
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far.

### ⚡ Constraints
- $-10^5 \\le num \\le 10^5$
- There will be at least one element in the data structure before calling `findMedian`.
- At most $5 \\times 10^4$ calls will be made to `addNum` and `findMedian`.
""",
        "starter_code": """class MedianFinder:
    def __init__(self):
        # Initialize your data structures here
        pass

    def addNum(self, num: int) -> None:
        pass

    def findMedian(self) -> float:
        pass
""",
        "solution_code": """import heapq

class MedianFinder:
    def __init__(self):
        # max_heap stores lower half (negated for Python's min-heap)
        self.small = []
        # min_heap stores upper half
        self.large = []

    def addNum(self, num: int) -> None:
        # Push to small (max-heap) first
        heapq.heappush(self.small, -num)

        # Invariant 1: every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Invariant 2: size balance: len(small) == len(large) or len(small) == len(large) + 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Dual Balancing Heaps
- **Time Complexity:** $\\mathcal{O}(\\log N)$ for `addNum`, $\\mathcal{O}(1)$ for `findMedian`.
- **Space Complexity:** $\\mathcal{O}(N)$ storing numbers split evenly across two heaps.

#### 💡 The Intuition
Split the sequence into two halves:
1. `small`: Max-heap storing the lower $\\lfloor N/2 \\rfloor$ elements.
2. `large`: Min-heap storing the upper $\\lceil N/2 \\rceil$ elements.
Every element in `small` is $\\le$ every element in `large`. If total elements are odd, `small` holds the median at its peak; if even, the median is the average of the two heap peaks!
""",
        "hints": {
            "nudge": "If you split the sorted numbers into two equal halves, which elements do you need to calculate the median?",
            "blueprint": "Maintain two heaps: a max-heap `small` for the smaller half and a min-heap `large` for the larger half. Ensure `len(small) == len(large)` or `len(small) == len(large) + 1`. Always maintain `max(small) <= min(large)`.",
            "master_scroll": "In `addNum`: push `-num` to `small`. If peaks violate `small <= large`, pop and swap. Rebalance so `len(small)` has at most 1 more element than `large`. In `findMedian`: return `-small[0]` if odd, else average of `-small[0]` and `large[0]`."
        },
        "sample_tests": [
            {
                "input": (
                    ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
                    [[], [1], [2], [], [3], []]
                ),
                "expected": [None, None, None, 1.5, None, 2.0],
                "display_input": "Commands: [addNum(1), addNum(2), findMedian(), addNum(3), findMedian()]"
            }
        ],
        "all_tests": [
            {
                "input": (
                    ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
                    [[], [1], [2], [], [3], []]
                ),
                "expected": [None, None, None, 1.5, None, 2.0]
            },
            {
                "input": (
                    ["MedianFinder", "addNum", "findMedian", "addNum", "findMedian", "addNum", "findMedian"],
                    [[], [5], [], [15], [], [1], []]
                ),
                "expected": [None, None, 5.0, None, 10.0, None, 5.0]
            },
            {
                "input": (
                    ["MedianFinder", "addNum", "addNum", "addNum", "addNum", "findMedian"],
                    [[], [-1], [-2], [-3], [-4], []]
                ),
                "expected": [None, None, None, None, None, -2.5]
            }
        ]
    },
    {
        "id": "word_ladder_ii",
        "title": "Word Ladder II",
        "boss_title": "BOSS 5: The Morphing Polyglot",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "findLadders",
        "problem_type": "function",
        "order_agnostic": True,
        "description": """
### 👹 Boss Dossier: The Morphing Polyglot
*The Morphing Polyglot encrypts the exit door with mutating lexical runes. You must discover ALL shortest mutation transformation sequences from `beginWord` to `endWord` changing only one letter at a time.*

### 📜 Problem Statement
A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:
- Every adjacent pair of words differs by a single letter.
- Every $s_i$ for $1 \\le i \\le k$ is in `wordList`. Note that `beginWord` does not need to be in `wordList`.
- $sk == endWord$

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return **all the shortest transformation sequences** from `beginWord` to `endWord`, or an empty list if no such sequence exists. Each sequence should be returned as a list of words `[beginWord, s1, s2, ..., sk]`.

### ⚡ Constraints
- $1 \\le \\text{len}(beginWord) \\le 5$
- $\\text{len}(endWord) == \\text{len}(beginWord)$
- $1 \\le \\text{len}(wordList) \\le 500$
- $\\text{len}(wordList[i]) == \\text{len}(beginWord)$
- All words consist of lowercase English letters.
- `beginWord != endWord`
""",
        "starter_code": """def findLadders(beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
    # Write your solution here
    pass
""",
        "solution_code": """from collections import defaultdict, deque

def findLadders(beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
    word_set = set(wordList)
    if endWord not in word_set:
        return []

    # BFS to construct parent graph and track shortest layer distances
    parents = defaultdict(set)
    layer = {beginWord}
    word_set.discard(beginWord)
    found = False

    while layer and not found:
        next_layer = set()
        visited_this_layer = set()
        for word in layer:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]
                    if next_word in word_set:
                        if next_word == endWord:
                            found = True
                        next_layer.add(next_word)
                        visited_this_layer.add(next_word)
                        parents[next_word].add(word)
        word_set -= visited_this_layer
        layer = next_layer

    if not found:
        return []

    # Backtrack DFS from endWord to beginWord
    res = []
    def dfs(word, path):
        if word == beginWord:
            res.append(path[::-1])
            return
        for p in parents[word]:
            dfs(p, path + [p])

    dfs(endWord, [endWord])
    return res
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Layered BFS + Reverse DFS Backtracking
- **Time Complexity:** $\\mathcal{O}(V + E)$ where $V = \\text{len}(wordList)$ and $E \\le 26 \\times L \\times V$.
- **Space Complexity:** $\\mathcal{O}(V \\times L)$ for parent graph and layers.

#### 💡 The Intuition
Directly storing all paths in a queue causes combinatorial explosion. Instead, use BFS level-by-level to construct a directed graph where each word maps to its valid predecessors in the shortest level (`parents[next_word].add(word)`). Once the destination level is reached, prune the search and use DFS backtracking from `endWord` back to `beginWord` to reconstruct only the shortest paths.
""",
        "hints": {
            "nudge": "Why does storing full paths in a standard BFS queue often result in Memory Limit Exceeded? Can you split the search into finding the shortest graph first, then reconstructing paths?",
            "blueprint": "Run a layer-by-layer BFS to build a `parents` mapping from child words to their valid predecessors on the preceding layer. Stop as soon as `endWord` is encountered in a layer. Then run DFS backtracking from `endWord` back to `beginWord`.",
            "master_scroll": "Use `layer = {beginWord}`. Expand valid single-letter mutations in `word_set`. Map `parents[next_word].add(word)`. Remove all words visited on the current layer from `word_set`. Once `endWord` reached, reconstruct all paths with recursive DFS from `endWord`."
        },
        "sample_tests": [
            {
                "input": ["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]],
                "expected": [["hit", "hot", "dot", "dog", "cog"], ["hit", "hot", "lot", "log", "cog"]],
                "display_input": "begin = 'hit', end = 'cog', wordList = ['hot','dot','dog','lot','log','cog']"
            },
            {
                "input": ["hit", "cog", ["hot", "dot", "dog", "lot", "log"]],
                "expected": [],
                "display_input": "begin = 'hit', end = 'cog', wordList = ['hot','dot','dog','lot','log']"
            }
        ],
        "all_tests": [
            {
                "input": ["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]],
                "expected": [["hit", "hot", "dot", "dog", "cog"], ["hit", "hot", "lot", "log", "cog"]]
            },
            {
                "input": ["hit", "cog", ["hot", "dot", "dog", "lot", "log"]],
                "expected": []
            },
            {
                "input": ["a", "c", ["a", "b", "c"]],
                "expected": [["a", "c"]]
            },
            {
                "input": ["red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"]],
                "expected": [["red", "ted", "tad", "tax"], ["red", "ted", "tex", "tax"], ["red", "rex", "tex", "tax"]]
            }
        ]
    },
    {
        "id": "max_profit_job_scheduling",
        "title": "Maximum Profit in Job Scheduling",
        "boss_title": "BOSS 6: The Chrono Mercenary",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "jobScheduling",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### 👹 Boss Dossier: The Chrono Mercenary
*A bounty board of mercenary cyber-contracts is available. Each contract occupies a non-interruptible temporal window $[startTime, endTime)$ and rewards net credits. You cannot accept overlapping contracts. Maximize your total payout.*

### 📜 Problem Statement
We have `n` jobs, where every job is scheduled to be done from `startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.
You're given the `startTime`, `endTime` and `profit` arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time ranges.
If you choose a job that ends at time `X` you will be able to start another job that starts at time `X`.

### ⚡ Constraints
- $1 \\le \\text{len}(startTime) == \\text{len}(endTime) == \\text{len}(profit) \\le 5 \\times 10^4$
- $1 \\le startTime[i] < endTime[i] \\le 10^9$
- $1 \\le profit[i] \\le 10^4$
""",
        "starter_code": """def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    # Write your solution here
    pass
""",
        "solution_code": """import bisect

def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
    # dp stores pairs of (endTime, max_profit_up_to_this_time)
    dp = [(0, 0)]

    for s, e, p in jobs:
        # Binary search for the latest job that ends <= s
        idx = bisect.bisect_right(dp, (s, float('inf'))) - 1
        prev_profit = dp[idx][1]
        current_profit = prev_profit + p

        if current_profit > dp[-1][1]:
            dp.append((e, current_profit))

    return dp[-1][1]
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: DP + Coordinate-Compressed Binary Search
- **Time Complexity:** $\\mathcal{O}(N \\log N)$ — Sorting jobs by end time and binary searching on disjoint intervals.
- **Space Complexity:** $\\mathcal{O}(N)$ for the monotonic DP history array.

#### 💡 The Intuition
Sort all jobs by their completion times `endTime`. For each job `(start, end, profit)`, you have two choices:
1. Don't take this job: Profit is the maximum profit achieved up to the previous job (`dp[-1]`).
2. Take this job: Profit is `profit + max_profit_before(start)`.
We locate the latest non-overlapping interval ending at or before `start` using binary search (`bisect_right`) in $\\mathcal{O}(\\log N)$ time. Append to `dp` only when a strictly better profit is achieved.
""",
        "hints": {
            "nudge": "If jobs are ordered chronologically by their completion time, what is the best non-overlapping job you could have completed right before starting the current one?",
            "blueprint": "Sort jobs by `endTime`. Maintain a list `dp = [(0, 0)]` of `(endTime, maxProfit)`. For each job `(s, e, p)`, use `bisect_right` on `dp` with time `s` to find the highest profit earned before time `s`. Compare `prev_profit + p` with `dp[-1][1]`.",
            "master_scroll": "Sort jobs by `endTime`. Loop over each job. Use `bisect.bisect_right(dp, (s, float('inf'))) - 1` to find non-overlapping historical state. If `prev_profit + p > dp[-1][1]`, append `(e, prev_profit + p)`. Return `dp[-1][1]`."
        },
        "sample_tests": [
            {"input": [[1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]], "expected": 120, "display_input": "start = [1,2,3,3], end = [3,4,5,6], profit = [50,10,40,70]"},
            {"input": [[1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]], "expected": 150, "display_input": "start = [1,2,3,4,6], end = [3,5,10,6,9], profit = [20,20,100,70,60]"},
            {"input": [[1, 1, 1], [2, 3, 4], [5, 6, 4]], "expected": 6, "display_input": "start = [1,1,1], end = [2,3,4], profit = [5,6,4]"},
        ],
        "all_tests": [
            {"input": [[1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]], "expected": 120},
            {"input": [[1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]], "expected": 150},
            {"input": [[1, 1, 1], [2, 3, 4], [5, 6, 4]], "expected": 6},
            {"input": [[4, 2, 4, 8, 2], [5, 5, 5, 10, 8], [12, 8, 10, 10, 100]], "expected": 110},
            {"input": [[1, 2, 2, 3], [2, 5, 3, 4], [3, 4, 1, 2]], "expected": 7},
        ]
    },
    {
        "id": "alien_dictionary",
        "title": "Alien Dictionary",
        "boss_title": "BOSS 7: The Extraterrestrial Oracle",
        "difficulty": "Hard",
        "category": "Boss Level / Hard",
        "xp": 500,
        "entry_point": "alienOrder",
        "problem_type": "function",
        "order_agnostic": False,
        "description": """
### 👹 Boss Dossier: The Extraterrestrial Oracle
*An ancient alien civilization left an encrypted lexicon of words sorted lexicographically according to their unknown alphabet. You must deduce the unique alphabetical ordering of their symbols or detect cyclic paradoxes.*

### 📜 Problem Statement
There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.
You are given a list of strings `words` from the alien language's dictionary. Now it is claimed that the strings in `words` are **sorted lexicographically** by the rules of this new language.

If this claim is incorrect, in that the strings cannot be sorted in any valid lexicographical order, return `""`.
Otherwise, return a string of the unique letters in the new alien language sorted in **lexicographically increasing order** by the new language's rules. If there are multiple solutions, return any of them.

### ⚡ Constraints
- $1 \\le \\text{len}(words) \\le 100$
- $1 \\le \\text{len}(words[i]) \\le 100$
- `words[i]` consists of only lowercase English letters.
""",
        "starter_code": """def alienOrder(words: list[str]) -> str:
    # Write your solution here
    pass
""",
        "solution_code": """from collections import defaultdict, deque

def alienOrder(words: list[str]) -> str:
    adj = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        # Edge case: Prefix violation like ["abc", "ab"]
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    # Kahn's algorithm (Topological sort BFS)
    queue = deque([c for c, deg in in_degree.items() if deg == 0])
    order = []

    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) < len(in_degree):
        return "" # Cycle detected

    return "".join(order)
""",
        "solution_explanation": """
### 🧠 Algorithmic Mastery: Directed Graph Topological Sort (Kahn's Algorithm)
- **Time Complexity:** $\\mathcal{O}(C)$ where $C$ is the total number of characters across all words.
- **Space Complexity:** $\\mathcal{O}(V + E)$ where $V \\le 26$ and $E \\le 26^2$.

#### 💡 The Intuition
Comparing adjacent words $w_1$ and $w_2$ at their first differing character gives a directed dependency $w_1[j] \\rightarrow w_2[j]$.
1. Check prefix edge case: if $w_1$ is longer than $w_2$ and begins with $w_2$, the ordering is invalid immediately (return `""`).
2. Build adjacency sets and calculate in-degrees for every unique character.
3. Perform Kahn's algorithm using a queue of zero in-degree nodes. If the resulting topological order contains fewer characters than the total unique set, a cycle exists (contradiction), so return `""`.
""",
        "hints": {
            "nudge": "How do lexicographical dictionaries establish precedence between adjacent words? What happens if you represent character precedence as directed graph edges?",
            "blueprint": "Build an adjacency list and `in_degree` map. Compare adjacent word pairs `words[i]` and `words[i+1]` to find the first differing character, creating a directed edge. Watch out for invalid prefixes like `['apple', 'app']`. Use Kahn's BFS algorithm for topological sort.",
            "master_scroll": "Initialize graph and in-degrees for all unique characters. For each adjacent pair, find first difference, add edge `u -> v` and increment `in_degree[v]`. Queue all characters with in-degree 0. While queue, pop and decrement neighbor in-degrees. If processed count < total unique characters, return empty string."
        },
        "sample_tests": [
            {"input": [["wrt", "wrf", "er", "ett", "rftt"]], "expected": "wertf", "display_input": "words = ['wrt', 'wrf', 'er', 'ett', 'rftt']"},
            {"input": [["z", "x"]], "expected": "zx", "display_input": "words = ['z', 'x']"},
            {"input": [["z", "x", "z"]], "expected": "", "display_input": "words = ['z', 'x', 'z']"},
        ],
        "all_tests": [
            {"input": [["wrt", "wrf", "er", "ett", "rftt"]], "expected": "wertf"},
            {"input": [["z", "x"]], "expected": "zx"},
            {"input": [["z", "x", "z"]], "expected": ""},
            {"input": [["abc", "ab"]], "expected": ""},
            {"input": [["z", "z"]], "expected": "z"},
            {"input": [["baa", "abcd", "abca", "cab", "cad"]], "expected": "bdac"},
        ]
    }
]


def get_all_problems() -> List[Dict[str, Any]]:
    return PROBLEMS


def get_problem_by_id(problem_id: str) -> Dict[str, Any]:
    for p in PROBLEMS:
        if p["id"] == problem_id:
            return p
    return PROBLEMS[0]


def get_problems_by_category(category: str) -> List[Dict[str, Any]]:
    if category == "All":
        return PROBLEMS
    return [p for p in PROBLEMS if p["category"] == category]


def get_problems_by_difficulty(diff: str) -> List[Dict[str, Any]]:
    if diff == "All":
        return PROBLEMS
    return [p for p in PROBLEMS if p["difficulty"] == diff]
