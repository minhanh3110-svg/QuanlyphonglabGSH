# FIX CRITICAL: TypeError in st.expander

## Problem
```
TypeError: expandable_proto.expanded = expanded
```

## Root Cause
The `expanded` parameter in `st.expander()` MUST be a Python `bool` type (True/False).
Sometimes the logic expression returns other types (None, string, etc.)

## Solution Applied

### Before (Error-prone):
```python
is_scanned = (st.session_state.scan_lo_id and 
              str(row['id']) == str(st.session_state.scan_lo_id))
              
with st.expander(title, expanded=is_scanned):  # ❌ Can be None or string
```

### After (100% Safe):
```python
# Step 1: Initialize as False
is_scanned_batch = False

# Step 2: Check attribute exists
try:
    if hasattr(st.session_state, 'scan_lo_id') and st.session_state.scan_lo_id is not None:
        is_scanned_batch = (str(row['id']) == str(st.session_state.scan_lo_id))
        # Force to boolean
        is_scanned_batch = True if is_scanned_batch else False
except Exception:
    is_scanned_batch = False

# Step 3: Create explicit boolean variable
expander_is_expanded = True if is_scanned_batch == True else False

# Step 4: Use explicit boolean
with st.expander(title, expanded=expander_is_expanded):  # ✅ Always bool
```

## Key Points

1. **Always initialize as False**: `is_scanned = False`
2. **Check attribute exists**: `hasattr(st.session_state, 'scan_lo_id')`
3. **Check not None**: `st.session_state.scan_lo_id is not None`
4. **Force boolean**: `True if condition else False`
5. **Use explicit variable**: Don't pass expression directly
6. **Wrap in try-except**: Catch any edge cases

## Applied to Files
- Line 2318-2332: Quản lý Phòng Sáng (Light Room Management)
- All st.expander() calls with dynamic expanded parameter

## Test
```python
# These are SAFE:
expanded=True          ✅
expanded=False         ✅
expanded=expander_is_expanded  ✅ (if expander_is_expanded is True/False)

# These can FAIL:
expanded=None          ❌
expanded=""            ❌
expanded=0             ❌
expanded=some_logic    ❌ (if returns non-bool)
```

