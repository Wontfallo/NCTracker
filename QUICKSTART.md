# NCTracker v2.0 - Quick Start Guide

## 🚀 Running the Application

```bash
# Navigate to project directory
cd c:\Users\WontML\Desktop\NCRTracker\NCTracker

# Run the application
streamlit run Home.py
```

## 🔑 Default Login

- **URL:** http://localhost:8501
- **Username:** `admin`
- **Password:** `admin123`

---

## 📱 Application Structure

### **Pages**
1. **🏠 Home** - Login page (Home.py)
2. **📊 Dashboard** - KPIs and overview
3. **🔍 NCR List** - Search and browse
4. **📄 NCR Detail** - View individual NCR
5. **🚪 Logout** - Sign out

### **Navigation**
- Use **sidebar** to switch between pages
- Click **emoji icons** for quick access
- **Breadcrumbs** show current location

---

## 🎨 Theme Features

### **Dark Mode (Default)**
- Professional dark background (#0B1220)
- High contrast text (#E5E7EB)
- Semantic status colors
- Smooth transitions

### **Components**
- **Metric Cards** - KPI displays with deltas
- **Status Badges** - Color-coded status indicators
- **NC Level Badges** - Priority level indicators
- **Info Boxes** - Contextual information
- **Empty States** - Helpful no-data messages

---

## 🔧 Component Quick Reference

### **Import Components**
```python
from components import (
    inject_theme_css,
    apply_plotly_theme,
    auth_guard,
    page_header,
    sidebar_brand,
    sidebar_user_info,
    metric_card,
    status_badge,
    nc_level_badge,
)
```

### **Page Template**
```python
import streamlit as st
from components import auth_guard, inject_theme_css

st.set_page_config(page_title="Page Title", layout="wide")
inject_theme_css()
auth_guard()

# Your page content here
```

### **Metric Card**
```python
metric_card(
    label="Total NCRs",
    value="42",
    delta="+5 this month",
    delta_color="positive",
    icon="📊"
)
```

### **Status Badge**
```python
st.markdown(status_badge("IN_PROGRESS"), unsafe_allow_html=True)
```

---

## 📊 Dashboard Features

### **KPI Cards**
- Total NCRs count
- Recent activity (last 30 days)
- Average resolution time
- Open NCRs count

### **Charts**
- **Status Distribution** - Donut chart
- **NC Level Distribution** - Bar chart
- All charts use dark theme

### **Recent NCRs Table**
- Shows last 15 NCRs
- Click to view details
- Quick filters available

---

## 🔍 NCR List Features

### **Search**
- Search by NCR number, title, or part number
- Real-time filtering
- Case-insensitive

### **Filters**
- **Status:** All, New, In Progress, Pending, Closed
- **NC Level:** All, 1-4
- **Sort:** Newest, Oldest, Number, Level

### **Actions**
- View details
- Refresh list
- Create new NCR

---

## 📄 NCR Detail Features

### **Tabs**
1. **Details** - Basic NCR information
2. **Level & CAPA** - NC level and CAPA details
3. **Investigation** - Problem analysis
4. **Correction** - Actions taken
5. **Closure** - Completion status
6. **Comments** - Discussion thread

### **Comments**
- View all comments
- Add new comments
- Timestamps and user names

---

## 🎯 Status Types

| Status | Badge Color | Icon |
|--------|-------------|------|
| NEW | Blue | 🆕 |
| IN_PROGRESS | Orange | ⚙️ |
| PENDING_APPROVAL | Pink | ⏳ |
| CLOSED | Green | ✅ |

---

## 🎚️ NC Levels

| Level | Severity | Color | Icon |
|-------|----------|-------|------|
| 1 | Critical | Red | 🔴 |
| 2 | Adverse | Orange | 🟠 |
| 3 | Moderate | Yellow | 🟡 |
| 4 | Low | Green | 🟢 |

---

## 🎨 CSS Variables Reference

### **Colors**
```css
--color-bg-0: #0B1220          /* Background */
--color-bg-1: #0E1526          /* Container */
--color-bg-2: #111827          /* Surface */
--color-text: #E5E7EB          /* Text */
--color-text-muted: #9CA3AF    /* Muted */
--color-primary-500: #6366F1   /* Primary */
--color-success: #22C55E       /* Success */
--color-warning: #F59E0B       /* Warning */
--color-error: #EF4444         /* Error */
```

### **Spacing**
```css
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-6: 24px
--space-8: 32px
```

### **Border Radius**
```css
--radius-sm: 6px
--radius: 8px
--radius-lg: 12px
--radius-xl: 16px
```

---

## 💡 Tips & Tricks

### **Performance**
- Use `@st.cache_data` for expensive operations
- Limit data displayed in tables
- Use pagination for large lists

### **Styling**
- Use CSS variables for consistency
- Follow the design system
- Test on different screen sizes

### **Development**
- Check browser console for errors
- Use Streamlit's debug mode
- Test auth guards on all pages

---

## 🐛 Troubleshooting

### **Can't Log In**
- Verify credentials: admin / admin123
- Check database exists
- Clear browser cache

### **Page Not Found**
- Ensure all page files exist in `pages/`
- Check file naming (must start with number)
- Verify imports are correct

### **Theme Not Loading**
- Check `assets/theme_dark.css` exists
- Verify `inject_theme_css()` is called
- Clear browser cache and reload

### **Charts Not Displaying**
- Call `apply_plotly_theme()` early
- Check Plotly is installed
- Verify data is not empty

---

## 📞 Getting Help

1. **Check README_v2.md** for detailed docs
2. **Review component code** in `components/`
3. **Check blueprint** in `ncr tracker.txt`
4. **Contact development team**

---

**Quick Start Version:** 1.0
**Last Updated:** November 6, 2025
