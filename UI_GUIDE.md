# Mandi Saathi - UI Guide

## Visual Overview

The Mandi Saathi interface embodies the **Harvest Clarity** design philosophy - a warm, trustworthy, and approachable experience inspired by agricultural heritage.

## Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  SIDEBAR (Deep Forest Green)    │  MAIN CONTENT         │
│  ┌──────────────────────────┐   │  ┌─────────────────┐ │
│  │ 🌾 Mandi Saathi          │   │  │ 🌾 Mandi Saathi │ │
│  │ YOUR NEGOTIATION...      │   │  │ Get Fair Prices │ │
│  ├──────────────────────────┤   │  └─────────────────┘ │
│  │ ➕ New Chat (Primary)    │   │                       │
│  ├──────────────────────────┤   │  ┌─────────────────┐ │
│  │ Recent Chats             │   │  │ Welcome Message │ │
│  │ 💬 Tomato - Ballia       │   │  │ (Warm Amber)    │ │
│  │ 💬 Onion - Nashik        │   │  └─────────────────┘ │
│  │ 💬 Potato - Agra         │   │                       │
│  └──────────────────────────┘   │  ┌─────────────────┐ │
│                                  │  │ User Message    │ │
│                                  │  │ (Soft Green)    │ │
│                                  │  └─────────────────┘ │
│                                  │  ┌─────────────────┐ │
│                                  │  │ Assistant Reply │ │
│                                  │  │ (White/Cream)   │ │
│                                  │  └─────────────────┘ │
│                                  │                       │
│                                  │  [Input Box]          │
└─────────────────────────────────────────────────────────┘
```

## Color Zones

### Sidebar (Left Panel)
- **Background**: Deep forest green gradient (#1B4332 → #2D6A4F)
- **Text**: Soft cream (#F8F6F3)
- **Buttons**: Emerald green with glow effect
- **Purpose**: Navigation and history, grounded and trustworthy

### Main Content (Right Panel)
- **Background**: Soft cream (#F8F6F3)
- **Cards**: White with subtle shadows
- **User Messages**: Light green gradient (#E8F5E9 → #D7F0DD)
- **Assistant Messages**: White with warm border
- **Purpose**: Clean, breathable space for conversation

## Component Showcase

### 1. Primary Button (New Chat)
```
┌────────────────────────┐
│  ➕ New Chat           │  ← Emerald green gradient
│                        │     Rounded corners (12px)
└────────────────────────┘     Soft shadow with glow
     ↓ Hover: Lifts up
```

### 2. Chat History Item
```
┌────────────────────────┐
│ 💬 Tomato - Ballia     │  ← Semi-transparent white
│ 📅 Jan 26 • 3 msgs     │     Slides right on hover
└────────────────────────┘
```

### 3. User Message
```
┌────────────────────────────────┐
│ Mera 5 quintal tamatar hai,    │  ← Light green gradient
│ trader 1500 bol raha hai       │     Left border: Emerald
└────────────────────────────────┘     Rounded (16px)
```

### 4. Assistant Message
```
┌────────────────────────────────┐
│ Bhai, abhi Ballia mein         │  ← White background
│ tamatar ka bhav ₹2800 chal     │     Left border: Harvest gold
│ raha hai...                    │     Rounded (16px)
└────────────────────────────────┘
```

### 5. Welcome Info Box
```
┌────────────────────────────────┐
│ 👋 Namaste! Welcome to         │  ← Warm amber gradient
│ Mandi Saathi                   │     Left border: Gold
│                                │     Soft shadow
│ I'm here to help you...        │
└────────────────────────────────┘
```

### 6. Input Field
```
┌────────────────────────────────┐
│ Type your message in any       │  ← White with green border
│ language...                    │     Rounded (16px)
└────────────────────────────────┘     Glows on focus
```

## Typography Hierarchy

### Main Title
```
🌾 Mandi Saathi
```
- Size: 2.5rem
- Weight: Bold (700)
- Color: Deep forest green (#1B4332)

### Subtitle
```
Get Fair Prices for Your Produce
```
- Size: 1.25rem
- Weight: Medium (500)
- Color: Sage green (#2D6A4F)

### Body Text
```
Regular conversation text
```
- Size: 1rem
- Weight: Regular (400)
- Color: Sage green (#2D6A4F)
- Line-height: 1.6

### Captions
```
📅 Jan 26 • 3 msgs
```
- Size: 0.75rem
- Weight: Light (300)
- Color: Light sage (#74A98A)
- Letter-spacing: 0.03em

## Interactive States

### Button Hover
- **Before**: Static position
- **After**: Lifts up 2px, enhanced shadow
- **Transition**: 0.3s ease

### Sidebar Item Hover
- **Before**: Aligned left
- **After**: Slides right 4px, brighter background
- **Transition**: 0.3s ease

### Input Focus
- **Before**: Light green border
- **After**: Emerald border, enhanced glow
- **Transition**: 0.3s ease

## Spacing System

### Vertical Rhythm
- Between messages: 1rem (16px)
- Between sections: 2rem (32px)
- Sidebar items: 0.5rem (8px)

### Padding
- Cards: 1.25rem (20px)
- Buttons: 0.75rem 1.5rem (12px 24px)
- Sidebar: 1.5rem 1rem (24px 16px)

## Shadows & Depth

### Elevation Levels

**Level 1** - Subtle (Chat messages)
```
0 2px 12px rgba(27, 67, 50, 0.08)
```

**Level 2** - Medium (Buttons)
```
0 4px 12px rgba(64, 145, 108, 0.3)
```

**Level 3** - Elevated (Input focus)
```
0 4px 20px rgba(82, 183, 136, 0.2)
```

## Responsive Behavior

### Desktop (> 1024px)
- Sidebar: 300px fixed width
- Main content: Centered, max 1200px
- Full feature set visible

### Tablet (768px - 1024px)
- Sidebar: Collapsible
- Main content: Full width
- Reduced padding

### Mobile (< 768px)
- Sidebar: Overlay/drawer
- Main content: Full width
- Compact spacing
- Touch-optimized buttons

## Accessibility Features

### Color Contrast
- All text meets WCAG AAA standards
- Minimum 7:1 contrast ratio
- Clear focus indicators

### Keyboard Navigation
- Tab through all interactive elements
- Enter to activate buttons
- Escape to close modals

### Screen Reader Support
- Semantic HTML structure
- ARIA labels where needed
- Descriptive button text

## Animation Principles

### Timing
- **Fast**: 0.15s (micro-interactions)
- **Standard**: 0.3s (most transitions)
- **Slow**: 0.5s (page transitions)

### Easing
- **ease**: Default for most
- **ease-in-out**: Smooth start and end
- **ease-out**: Natural deceleration

### Movement
- Subtle lifts (2-4px)
- Gentle slides (4-8px)
- No jarring jumps

## Design Tokens

```css
/* Colors */
--forest-green: #1B4332;
--emerald-green: #52B788;
--sage-green: #40916C;
--harvest-gold: #D4A574;
--soft-cream: #F8F6F3;
--light-sage: #95D5B2;
--mint: #B7E4C7;

/* Spacing */
--space-xs: 0.5rem;
--space-sm: 1rem;
--space-md: 1.5rem;
--space-lg: 2rem;
--space-xl: 3rem;

/* Border Radius */
--radius-sm: 10px;
--radius-md: 12px;
--radius-lg: 16px;

/* Shadows */
--shadow-subtle: 0 2px 8px rgba(27, 67, 50, 0.08);
--shadow-medium: 0 2px 12px rgba(27, 67, 50, 0.08);
--shadow-elevated: 0 4px 16px rgba(27, 67, 50, 0.1);
```

## Best Practices

### Do's ✅
- Use generous white space
- Maintain consistent border radius
- Apply warm-tinted shadows
- Keep text concise and clear
- Use icons for visual interest
- Ensure smooth transitions

### Don'ts ❌
- Don't use sharp corners
- Avoid cold gray shadows
- Don't overcrowd the interface
- Avoid harsh color contrasts
- Don't use too many fonts
- Avoid jarring animations

## Implementation Notes

### Streamlit Customization
- Custom CSS via `st.markdown()`
- Theme config in `.streamlit/config.toml`
- Component styling via data-testid selectors

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Graceful degradation for older browsers
- Mobile-optimized touch targets

### Performance
- Minimal animations (only on interaction)
- Optimized gradients and shadows
- Efficient CSS selectors
- Lazy loading for chat history

---

**UI Guide Version**: 1.0  
**Design System**: Harvest Clarity  
**Last Updated**: January 2024
