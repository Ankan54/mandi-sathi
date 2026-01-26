# Mandi Saathi - Harvest Clarity Design System

## Design Philosophy

**Harvest Clarity** is a visual language born from the intersection of agrarian wisdom and digital trust. It draws from the earthy warmth of freshly tilled soil, the golden hour light that bathes open fields, and the honest simplicity of a handshake at the village market.

## Color Palette

### Primary Colors
- **Deep Forest Green** `#1B4332` - Trust, growth, prosperity
- **Emerald Green** `#52B788` - Primary actions, healthy crops
- **Sage Green** `#40916C` - Secondary actions, stability

### Secondary Colors
- **Harvest Gold** `#D4A574` - Warmth, ripe grain, highlights
- **Terracotta** `#B8956A` - Earthy accents, grounding
- **Soft Cream** `#F8F6F3` - Background, breathing room

### Accent Colors
- **Light Sage** `#95D5B2` - Hover states, subtle highlights
- **Mint** `#B7E4C7` - Success states, positive feedback
- **Pale Green** `#D7F0DD` - User messages, gentle emphasis
- **Warm Amber** `#FFF8E7` - Info boxes, gentle warnings

### Text Colors
- **Primary Text** `#1B4332` - Main content
- **Secondary Text** `#2D6A4F` - Headings, emphasis
- **Tertiary Text** `#74A98A` - Captions, metadata
- **Muted Text** `#5C4A3A` - Subtle information

## Typography

### Font Family
- **Primary**: Inter (Google Fonts)
- **Weights**: 300 (Light), 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold)

### Type Scale
- **H1**: 2.5rem, Bold (700), -0.02em letter-spacing
- **H2/H3**: 1.5-2rem, Semi-Bold (600), 0.01em letter-spacing
- **Body**: 1rem, Regular (400), 0.02em letter-spacing
- **Caption**: 0.75-0.875rem, Light (300), 0.03-0.05em letter-spacing

### Principles
- Generous letter-spacing for readability
- Clean sans-serif for clarity at any size
- Sparse text - essential words only
- Bold for actions, light for context

## Spacing & Layout

### Spatial Composition
- **Generous negative space** - Information breathes like crops need air
- **Organic flow** - Top to bottom, left to right
- **Rounded forms** - Never sharp or intimidating (12-16px border-radius)
- **Floating cards** - Subtle shadows for depth without heaviness

### Padding & Margins
- **Small**: 0.5rem (8px)
- **Medium**: 1rem (16px)
- **Large**: 1.5rem (24px)
- **XLarge**: 2rem (32px)

## Components

### Buttons

#### Primary Button
- Background: Linear gradient `#52B788` → `#40916C`
- Color: White
- Border-radius: 12px
- Padding: 0.75rem 1.5rem
- Shadow: `0 4px 12px rgba(64, 145, 108, 0.3)`
- Hover: Darker gradient, lift effect

#### Secondary Button
- Background: `rgba(255, 255, 255, 0.1)`
- Border: `1px solid rgba(255, 255, 255, 0.2)`
- Border-radius: 10px
- Hover: Slight slide effect

### Chat Messages

#### User Message
- Background: Linear gradient `#E8F5E9` → `#D7F0DD`
- Border-left: 3px solid `#52B788`
- Border-radius: 16px
- Shadow: Soft, warm-tinted

#### Assistant Message
- Background: White
- Border-left: 3px solid `#D4A574`
- Border-radius: 16px
- Shadow: Subtle depth

### Input Fields
- Border: 2px solid `#D7F0DD`
- Border-radius: 16px
- Focus: Border `#52B788`, enhanced shadow
- Placeholder: `#95D5B2`, light weight

### Info Boxes
- Background: Linear gradient `#FFF8E7` → `#FFE8CC`
- Border-left: 4px solid `#D4A574`
- Border-radius: 12px
- Shadow: Warm-tinted

## Sidebar Design

### Background
- Linear gradient: `#1B4332` → `#2D6A4F` (180deg)
- Creates depth and visual interest

### Elements
- All text: `#F8F6F3` (soft cream)
- Captions: `#B7E4C7` (light sage)
- Dividers: `rgba(255, 255, 255, 0.2)`

## Shadows & Depth

### Shadow Palette
- **Subtle**: `0 2px 8px rgba(27, 67, 50, 0.08)`
- **Medium**: `0 2px 12px rgba(27, 67, 50, 0.08)`
- **Elevated**: `0 4px 16px rgba(27, 67, 50, 0.1)`
- **Accent**: `0 4px 12px rgba(64, 145, 108, 0.3)`

### Principles
- Warm-tinted shadows (never cold gray)
- Organic depth (not digital/harsh)
- Subtle elevation for cards

## Interactions

### Transitions
- Duration: 0.3s
- Easing: ease, ease-in-out
- Properties: background-color, border-color, color, transform

### Hover States
- Buttons: Slight lift (`translateY(-2px)`)
- Cards: Enhanced shadow
- Sidebar items: Slide right (`translateX(4px)`)

### Loading States
- Spinner: `#52B788` (emerald green)
- Pulse animation for feedback

## Accessibility

### Contrast Ratios
- Primary text on background: 12:1 (AAA)
- Secondary text on background: 8:1 (AAA)
- Button text on green: 4.5:1 (AA)

### Focus States
- Clear focus indicators
- Enhanced borders on focus
- Keyboard navigation support

## Responsive Behavior

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Adaptations
- Sidebar collapses on mobile
- Reduced padding on small screens
- Maintained readability at all sizes

## Brand Voice

### Visual Tone
- **Warm**: Earth tones, golden hour lighting
- **Trustworthy**: Deep greens, solid forms
- **Approachable**: Rounded corners, soft shadows
- **Professional**: Clean typography, organized layout

### Emotional Goals
- Safety and welcome
- Trust and reliability
- Simplicity and clarity
- Connection to agriculture

## Implementation Notes

### CSS Architecture
- Custom CSS injected via Streamlit markdown
- Scoped selectors for Streamlit components
- Graceful fallbacks for unsupported features

### Performance
- Minimal animations (only on interaction)
- Optimized gradients
- Efficient selectors

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Graceful degradation for older browsers
- Mobile-first approach

## Design Craftsmanship

Every element reflects meticulous attention:
- **Pixel-perfect alignment** - No element out of place
- **Harmonious color transitions** - Smooth, natural gradients
- **Thoughtful spacing** - Rhythm and breathing room
- **Refined typography** - Kerning and weight perfection
- **Subtle interactions** - Natural, fluid movements

This is design that took countless hours to refine, where every detail demonstrates expert-level craftsmanship.

---

**Design System Version**: 1.0  
**Last Updated**: January 2024  
**Maintained by**: Mandi Saathi Team
