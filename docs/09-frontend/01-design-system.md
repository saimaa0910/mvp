# Namma Clinic Frontend Design System Specification

## 1. Executive Summary & Design System Philosophy
The Namma Clinic Digital Health & Operations Platform serves as the frontline clinical and public health interface for 183 primary healthcare centers across the Greater Bengaluru Authority (GBA) / Bruhat Bengaluru Mahanagara Palike (BBMP). The design system, codenamed **'Arogya Bandhu UI'**, establishes an enterprise-grade, accessible, high-contrast, bilingual design architecture tailored specifically for municipal outpatient clinics operating in high-volume, noisy, and occasionally resource-constrained urban environments.

### 1.1 Core Design Pillars
- **Clinical Velocity & Ergonomics:** Minimizing clicks, tab traversals, and visual clutter for doctors and staff nurses seeing 80–120 patients per outpatient shift.
- **Kannada-First Equity:** Full linguistic parity between Kannada (ಕನ್ನಡ) and English, supporting clear display of complex ligatures, medical transliterations, and thermal print legibility.
- **Cognitive Safety & Fail-Safe Alerts:** Unambiguous visual differentiation between emergency danger signs (red alerts), priority triage cases (yellow), and routine outpatient consultations (green/blue).
- **Offline & Hardware Resiliency:** Graceful visual state degradation when operating offline on clinic mini-PCs, supporting keyboard-only navigation and thermal receipt printing.
- **Universal Accessibility (WCAG 2.1 AA):** High-contrast ratios (minimum 4.5:1 for normal text, 7:1 in enhanced high-contrast mode), large touch targets (minimum 44x44px for clinic tablets), and comprehensive ARIA live regions.

## 2. Design Tokens: Typography System
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export const TYPOGRAPHY_TOKENS = {
  fontFamily: {
    kannadaPrimary: 'Noto Sans Kannada, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
    kannadaSerif: 'Noto Serif Kannada, Georgia, serif',
    englishPrimary: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
    clinicalMono: 'JetBrains Mono, Fira Code, Menlo, monospace'
  },
  fontSize: {
    xs: '0.75rem',    // 12px - Table metadata, footnotes
    sm: '0.875rem',   // 14px - Standard input labels, table cell content
    base: '1.0rem',   // 16px - Body text, clinical consultation notes
    lg: '1.125rem',   // 18px - Card headings, token callouts
    xl: '1.25rem',    // 20px - Section sub-headers, vitals values
    '2xl': '1.5rem',  // 24px - Screen titles, primary modal headers
    '3xl': '1.875rem',// 30px - Waiting queue token numbers
    '4xl': '2.25rem'  // 36px - Emergency public display alerts
  },
  lineHeight: {
    tight: '1.2',     // Display headings and vitals digits
    kannada: '1.6',   // Relaxed line-height to accommodate Kannada matras and vottakshara
    normal: '1.5',    // Standard English prose
    relaxed: '1.75'   // Patient instructions and clinical counseling text
  },
  fontWeight: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700
  }
};
```

## 3. Design Tokens: Color Semantics & Clinical Palettes
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export const COLOR_TOKENS = {
  brand: {
    primary: '#005A9C',       // BBMP Healthcare Royal Blue
    primaryHover: '#004070',
    primaryActive: '#002B4C',
    primarySurface: '#EBF4FA', // Tinted card background
    secondary: '#00875A',     // Karnataka Health Department Emerald
    accent: '#FF7A00'         // Warm saffron accent
  },
  clinical: {
    emergencyRed: '#DE350B',   // MEWS > 5, Systolic > 180, Hypoxia < 90%
    warningYellow: '#FFAB00',  // Priority triage, low stock, allergy conflict
    stableGreen: '#00875A',    // Normal vitals, dispensed, synced
    infoBlue: '#0065FF',       // Standard appointment, follow-up scheduled
    quarantinePurple: '#6554C0' // Expired batches, specialized infectious ward
  },
  neutrals: {
    background: '#F8FAFC',
    surface: '#FFFFFF',
    surfaceMuted: '#F1F5F9',
    border: '#E2E8F0',
    borderStrong: '#CBD5E1',
    textPrimary: '#0F172A',
    textSecondary: '#475569',
    textDisabled: '#94A3B8'
  },
  highContrast: {
    background: '#000000',
    surface: '#121212',
    border: '#FFFF00',        // Vivid yellow border for low-vision navigation
    textPrimary: '#FFFFFF',
    emergencyRed: '#FF4D4D',
    stableGreen: '#33FF33'
  }
};
```

## 4. Spacing, Elevation & Layout Primitives
The layout system is constructed around a strict **4px/8px modular grid** ensuring consistent touch-target sizes, visual cadence, and alignment across diverse display form factors.

| Token Name | Value | Physical Dimension | Primary Clinical Application |
| :--- | :--- | :--- | :--- |
| `spacing.xxs` | 0.125rem | 2px | Table cell internal borders, divider strokes |
| `spacing.xs` | 0.25rem | 4px | Tag padding, icon-to-label gaps, badge margins |
| `spacing.sm` | 0.5rem | 8px | Button internal padding, input padding, chip clusters |
| `spacing.md` | 0.75rem | 12px | Compact form row gaps, card sub-section spacing |
| `spacing.base` | 1.0rem | 16px | Standard card padding, modal body margin, form group gaps |
| `spacing.lg` | 1.5rem | 24px | Major section margins, consultation pane dividers |
| `spacing.xl` | 2.0rem | 32px | Page header spacing, dashboard widget gaps |
| `spacing.2xl` | 3.0rem | 48px | Screen boundary margins on 1080p desktop monitors |
| `spacing.3xl` | 4.0rem | 64px | Empty state illustrative breathing space |

## 5. Comprehensive Component Design Specifications
The design system provides standardized architectural guidelines, interactive states, accessibility bindings, and Kannada localization rules for all 160 planned components across the 11 functional tiers.

### COMP-001: AppShell
**Category:** Layout & Navigation | **Component Identifier:** `COMP-001`

#### Purpose & Clinical Function
The `AppShell` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Master application container with responsive header, collapsible sidebar, and offline banner. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AppShellProps {
  id: string; // Unique DOM element identifier matching 'COMP-001'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-002: ClinicHeader
**Category:** Layout & Navigation | **Component Identifier:** `COMP-002`

#### Purpose & Clinical Function
The `ClinicHeader` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Top navigation bar showing clinic name, ward code, active doctor name, sync badge, and language toggle. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicHeaderProps {
  id: string; // Unique DOM element identifier matching 'COMP-002'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-003: RoleSidebar
**Category:** Layout & Navigation | **Component Identifier:** `COMP-003`

#### Purpose & Clinical Function
The `RoleSidebar` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Dynamic sidebar rendering only permitted navigation routes based on active user role. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RoleSidebarProps {
  id: string; // Unique DOM element identifier matching 'COMP-003'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-004: BreadcrumbNav
**Category:** Layout & Navigation | **Component Identifier:** `COMP-004`

#### Purpose & Clinical Function
The `BreadcrumbNav` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Hierarchical navigation trail with deep-link support and keyboard tab focus. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BreadcrumbNavProps {
  id: string; // Unique DOM element identifier matching 'COMP-004'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-005: TabBar
**Category:** Layout & Navigation | **Component Identifier:** `COMP-005`

#### Purpose & Clinical Function
The `TabBar` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Multi-tab sub-navigation for clinical encounters and patient longitudinal record sections. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TabBarProps {
  id: string; // Unique DOM element identifier matching 'COMP-005'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-006: SplitPaneLayout
**Category:** Layout & Navigation | **Component Identifier:** `COMP-006`

#### Purpose & Clinical Function
The `SplitPaneLayout` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Dual-pane responsive layout for simultaneous patient record view and consultation notes entry. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SplitPaneLayoutProps {
  id: string; // Unique DOM element identifier matching 'COMP-006'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-007: PageContainer
**Category:** Layout & Navigation | **Component Identifier:** `COMP-007`

#### Purpose & Clinical Function
The `PageContainer` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Standard content wrapper enforcing responsive margins, maximum width, and padding. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PageContainerProps {
  id: string; // Unique DOM element identifier matching 'COMP-007'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-008: ActionToolbar
**Category:** Layout & Navigation | **Component Identifier:** `COMP-008`

#### Purpose & Clinical Function
The `ActionToolbar` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Sticky action bar with primary CTA, secondary actions, and cancel/back buttons. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ActionToolbarProps {
  id: string; // Unique DOM element identifier matching 'COMP-008'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-009: MobileBottomNav
**Category:** Layout & Navigation | **Component Identifier:** `COMP-009`

#### Purpose & Clinical Function
The `MobileBottomNav` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Bottom icon bar optimized for tablet and handheld mobile screens. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MobileBottomNavProps {
  id: string; // Unique DOM element identifier matching 'COMP-009'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-010: DrawerContainer
**Category:** Layout & Navigation | **Component Identifier:** `COMP-010`

#### Purpose & Clinical Function
The `DrawerContainer` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Slide-out side drawer for quick patient summary, sync queue, or notifications. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DrawerContainerProps {
  id: string; // Unique DOM element identifier matching 'COMP-010'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-011: CollapsibleSection
**Category:** Layout & Navigation | **Component Identifier:** `COMP-011`

#### Purpose & Clinical Function
The `CollapsibleSection` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Accordion card with smooth expansion toggle and ARIA expanded state. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CollapsibleSectionProps {
  id: string; // Unique DOM element identifier matching 'COMP-011'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-012: CardSurface
**Category:** Layout & Navigation | **Component Identifier:** `COMP-012`

#### Purpose & Clinical Function
The `CardSurface` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Elevated visual card container with standardized borders, radius, and shadows. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CardSurfaceProps {
  id: string; // Unique DOM element identifier matching 'COMP-012'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-013: ModalContainer
**Category:** Layout & Navigation | **Component Identifier:** `COMP-013`

#### Purpose & Clinical Function
The `ModalContainer` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Accessible modal dialog overlay with focus trap, backdrop blur, and escape key listener. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ModalContainerProps {
  id: string; // Unique DOM element identifier matching 'COMP-013'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-014: KeyboardShortcutGuide
**Category:** Layout & Navigation | **Component Identifier:** `COMP-014`

#### Purpose & Clinical Function
The `KeyboardShortcutGuide` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Floating cheat sheet displaying fast-action keyboard shortcuts for clinical workflows. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface KeyboardShortcutGuideProps {
  id: string; // Unique DOM element identifier matching 'COMP-014'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-015: FooterStatusStrip
**Category:** Layout & Navigation | **Component Identifier:** `COMP-015`

#### Purpose & Clinical Function
The `FooterStatusStrip` component operates as a primary UI primitive within the Layout & Navigation functional boundary. Bottom status strip displaying local SQLite sync state, memory usage, and software version. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Layout & Navigation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FooterStatusStripProps {
  id: string; // Unique DOM element identifier matching 'COMP-015'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-016: StatusBadge
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-016`

#### Purpose & Clinical Function
The `StatusBadge` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Color-coded status chip for visit states, lab statuses, and triage urgency tiers. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StatusBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-016'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-017: ToastNotification
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-017`

#### Purpose & Clinical Function
The `ToastNotification` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Auto-dismissing toast alert with success, warning, error, and info styles. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ToastNotificationProps {
  id: string; // Unique DOM element identifier matching 'COMP-017'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-018: SystemAlertBanner
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-018`

#### Purpose & Clinical Function
The `SystemAlertBanner` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Prominent full-width alert banner for network disconnection or emergency alerts. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SystemAlertBannerProps {
  id: string; // Unique DOM element identifier matching 'COMP-018'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-019: EmptyStateDisplay
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-019`

#### Purpose & Clinical Function
The `EmptyStateDisplay` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Illustrative placeholder with descriptive text and clear primary action button. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface EmptyStateDisplayProps {
  id: string; // Unique DOM element identifier matching 'COMP-019'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-020: LoadingSkeletonCard
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-020`

#### Purpose & Clinical Function
The `LoadingSkeletonCard` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Shimmering animated skeleton placeholder matching target content geometry. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LoadingSkeletonCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-020'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-021: LoadingSpinner
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-021`

#### Purpose & Clinical Function
The `LoadingSpinner` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Lightweight SVG circular activity indicator with accessible aria-busy announce. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LoadingSpinnerProps {
  id: string; // Unique DOM element identifier matching 'COMP-021'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-022: LinearProgressBar
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-022`

#### Purpose & Clinical Function
The `LinearProgressBar` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Determinate and indeterminate progress bar for batch operations and sync progress. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LinearProgressBarProps {
  id: string; // Unique DOM element identifier matching 'COMP-022'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-023: MetricStatCard
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-023`

#### Purpose & Clinical Function
The `MetricStatCard` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. KPI stat card displaying numerical figure, trend sparkline, and percentage change. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MetricStatCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-023'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-024: DataTableGrid
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-024`

#### Purpose & Clinical Function
The `DataTableGrid` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. High-performance virtualized table supporting sorting, filtering, and column resize. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DataTableGridProps {
  id: string; // Unique DOM element identifier matching 'COMP-024'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-025: PaginationControl
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-025`

#### Purpose & Clinical Function
The `PaginationControl` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Accessible pagination toolbar with page jump, size selector, and item counts. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PaginationControlProps {
  id: string; // Unique DOM element identifier matching 'COMP-025'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-026: ConfirmationDialog
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-026`

#### Purpose & Clinical Function
The `ConfirmationDialog` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Destructive action confirmation modal with explicit hazard warning and dual confirmation. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ConfirmationDialogProps {
  id: string; // Unique DOM element identifier matching 'COMP-026'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-027: TooltipWrapper
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-027`

#### Purpose & Clinical Function
The `TooltipWrapper` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Hover and focus triggered tooltip providing micro-help in Kannada and English. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TooltipWrapperProps {
  id: string; // Unique DOM element identifier matching 'COMP-027'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-028: PopoverMenu
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-028`

#### Purpose & Clinical Function
The `PopoverMenu` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Contextual action popover menu positioned dynamically next to trigger element. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PopoverMenuProps {
  id: string; // Unique DOM element identifier matching 'COMP-028'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-029: TagCloud
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-029`

#### Purpose & Clinical Function
The `TagCloud` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Interactive collection of chips for symptom tags, allergy labels, and diagnosis tags. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TagCloudProps {
  id: string; // Unique DOM element identifier matching 'COMP-029'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-030: AuditDiffViewer
**Category:** Data Display & Feedback | **Component Identifier:** `COMP-030`

#### Purpose & Clinical Function
The `AuditDiffViewer` component operates as a primary UI primitive within the Data Display & Feedback functional boundary. Side-by-side visual diff component showing before-and-after state changes in records. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Data Display & Feedback` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AuditDiffViewerProps {
  id: string; // Unique DOM element identifier matching 'COMP-030'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-031: TextInput
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-031`

#### Purpose & Clinical Function
The `TextInput` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Single-line text input with floating label, validation error icon, and clear button. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TextInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-031'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-032: MaskedPhoneInput
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-032`

#### Purpose & Clinical Function
The `MaskedPhoneInput` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Indian 10-digit mobile number input with +91 prefix and automatic formatting. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MaskedPhoneInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-032'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-033: AadhaarMaskedInput
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-033`

#### Purpose & Clinical Function
The `AadhaarMaskedInput` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. 12-digit national ID input with automated masking (XXXX-XXXX-1234) for privacy. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AadhaarMaskedInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-033'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-034: NumberInputStepper
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-034`

#### Purpose & Clinical Function
The `NumberInputStepper` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Numeric input with increment/decrement steppers and min/max clamping. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NumberInputStepperProps {
  id: string; // Unique DOM element identifier matching 'COMP-034'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-035: SearchableCombobox
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-035`

#### Purpose & Clinical Function
The `SearchableCombobox` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Autocomplete dropdown with asynchronous search, keyboard navigation, and create-new option. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SearchableComboboxProps {
  id: string; // Unique DOM element identifier matching 'COMP-035'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-036: SingleSelectDropdown
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-036`

#### Purpose & Clinical Function
The `SingleSelectDropdown` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Standard select menu with native mobile fallback and accessible keyboard navigation. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SingleSelectDropdownProps {
  id: string; // Unique DOM element identifier matching 'COMP-036'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-037: MultiSelectCheckboxDropdown
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-037`

#### Purpose & Clinical Function
The `MultiSelectCheckboxDropdown` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Dropdown enabling multiple checkbox selections with selected count badges. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MultiSelectCheckboxDropdownProps {
  id: string; // Unique DOM element identifier matching 'COMP-037'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-038: DatePickerCalendar
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-038`

#### Purpose & Clinical Function
The `DatePickerCalendar` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Accessible calendar popup supporting date selection with Kannada month labels. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DatePickerCalendarProps {
  id: string; // Unique DOM element identifier matching 'COMP-038'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-039: TimePickerControl
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-039`

#### Purpose & Clinical Function
The `TimePickerControl` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. 12/24 hour time selector with AM/PM toggle and quick-select presets. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TimePickerControlProps {
  id: string; // Unique DOM element identifier matching 'COMP-039'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-040: RadioGroupSelector
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-040`

#### Purpose & Clinical Function
The `RadioGroupSelector` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Accessible radio button group with arrow key navigation and label descriptions. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RadioGroupSelectorProps {
  id: string; // Unique DOM element identifier matching 'COMP-040'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-041: CheckboxControl
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-041`

#### Purpose & Clinical Function
The `CheckboxControl` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Standard checkbox with custom checkmark icon, indeterminate state, and error styling. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CheckboxControlProps {
  id: string; // Unique DOM element identifier matching 'COMP-041'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-042: ToggleSwitch
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-042`

#### Purpose & Clinical Function
The `ToggleSwitch` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Binary on/off toggle switch with smooth sliding animation and high-contrast focus ring. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ToggleSwitchProps {
  id: string; // Unique DOM element identifier matching 'COMP-042'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-043: TextAreaInput
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-043`

#### Purpose & Clinical Function
The `TextAreaInput` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Multi-line text area with auto-expansion, character counter, and spellcheck toggle. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TextAreaInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-043'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-044: DigitalSignaturePad
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-044`

#### Purpose & Clinical Function
The `DigitalSignaturePad` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. HTML5 canvas signature pad for citizen consent and clinician sign-off with clear/undo. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DigitalSignaturePadProps {
  id: string; // Unique DOM element identifier matching 'COMP-044'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-045: WebcamCaptureWidget
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-045`

#### Purpose & Clinical Function
The `WebcamCaptureWidget` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Browser webcam interface with face guide overlay, capture snapshot, and retake controls. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface WebcamCaptureWidgetProps {
  id: string; // Unique DOM element identifier matching 'COMP-045'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-046: BarcodeScannerInput
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-046`

#### Purpose & Clinical Function
The `BarcodeScannerInput` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Hardware HID barcode scanner listener with debounce and audio beep feedback. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BarcodeScannerInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-046'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-047: FileUploadDropzone
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-047`

#### Purpose & Clinical Function
The `FileUploadDropzone` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Drag-and-drop document upload area with file size validation and thumbnail preview. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FileUploadDropzoneProps {
  id: string; // Unique DOM element identifier matching 'COMP-047'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-048: PasswordInput
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-048`

#### Purpose & Clinical Function
The `PasswordInput` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Secure password field with visibility toggle, strength meter, and caps-lock warning. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PasswordInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-048'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-049: FormActionFooter
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-049`

#### Purpose & Clinical Function
The `FormActionFooter` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Standardized form button row with Submit, Reset, and Save Draft buttons. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FormActionFooterProps {
  id: string; // Unique DOM element identifier matching 'COMP-049'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-050: FieldValidationError
**Category:** Form Controls & Inputs | **Component Identifier:** `COMP-050`

#### Purpose & Clinical Function
The `FieldValidationError` component operates as a primary UI primitive within the Form Controls & Inputs functional boundary. Accessible inline error message with role='alert' and SVG warning icon. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Form Controls & Inputs` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FieldValidationErrorProps {
  id: string; // Unique DOM element identifier matching 'COMP-050'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-051: PatientBanner
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-051`

#### Purpose & Clinical Function
The `PatientBanner` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Persistent patient header displaying UHID, photo, name, age/gender, allergies, and vitals. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PatientBannerProps {
  id: string; // Unique DOM element identifier matching 'COMP-051'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-052: VitalsGridDisplay
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-052`

#### Purpose & Clinical Function
The `VitalsGridDisplay` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Structured grid displaying current visit vitals with abnormal value highlighting. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VitalsGridDisplayProps {
  id: string; // Unique DOM element identifier matching 'COMP-052'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-053: VitalsTrendSparkline
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-053`

#### Purpose & Clinical Function
The `VitalsTrendSparkline` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Miniature line chart showing systolic BP or blood sugar trend across past 5 visits. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VitalsTrendSparklineProps {
  id: string; // Unique DOM element identifier matching 'COMP-053'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-054: DangerScoreBadge
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-054`

#### Purpose & Clinical Function
The `DangerScoreBadge` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Early Warning Score (MEWS/PEWS) color-coded badge indicating clinical risk level. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DangerScoreBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-054'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-055: AllergyAlertChip
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-055`

#### Purpose & Clinical Function
The `AllergyAlertChip` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. High-visibility red warning chip highlighting confirmed drug allergies on hover/click. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AllergyAlertChipProps {
  id: string; // Unique DOM element identifier matching 'COMP-055'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-056: DiagnosisSearchCombobox
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-056`

#### Purpose & Clinical Function
The `DiagnosisSearchCombobox` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Dual-search ICD-10 and SNOMED CT diagnosis selector with Kannada common terms. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DiagnosisSearchComboboxProps {
  id: string; // Unique DOM element identifier matching 'COMP-056'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-057: ChiefComplaintSelector
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-057`

#### Purpose & Clinical Function
The `ChiefComplaintSelector` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Interactive body map and common complaints grid for rapid symptom logging. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ChiefComplaintSelectorProps {
  id: string; // Unique DOM element identifier matching 'COMP-057'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-058: ClinicalHistoryTimeline
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-058`

#### Purpose & Clinical Function
The `ClinicalHistoryTimeline` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Vertical timeline depicting past diagnoses, prescriptions, and lab tests chronologically. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicalHistoryTimelineProps {
  id: string; // Unique DOM element identifier matching 'COMP-058'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-059: ConsultationTimer
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-059`

#### Purpose & Clinical Function
The `ConsultationTimer` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Discreet timer tracking duration of patient encounter for clinic workflow analytics. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ConsultationTimerProps {
  id: string; // Unique DOM element identifier matching 'COMP-059'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-060: PediatricPercentileCard
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-060`

#### Purpose & Clinical Function
The `PediatricPercentileCard` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. WHO child growth percentile card plotting weight-for-age and height-for-age. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PediatricPercentileCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-060'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-061: ANCEncounterCard
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-061`

#### Purpose & Clinical Function
The `ANCEncounterCard` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Antenatal care tracker displaying trimester, expected delivery date, and high-risk flags. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ANCEncounterCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-061'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-062: NCDTrackingCard
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-062`

#### Purpose & Clinical Function
The `NCDTrackingCard` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Chronic illness management summary displaying 3-month HbA1c and BP control metrics. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NCDTrackingCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-062'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-063: ClinicalNoteEditor
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-063`

#### Purpose & Clinical Function
The `ClinicalNoteEditor` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Rich text SOAP clinical note editor with pre-filled physical examination templates. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicalNoteEditorProps {
  id: string; // Unique DOM element identifier matching 'COMP-063'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-064: DrugAllergyModal
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-064`

#### Purpose & Clinical Function
The `DrugAllergyModal` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Formal modal for recording new drug or food allergies with reaction severity. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DrugAllergyModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-064'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-065: BreakGlassAlertBanner
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-065`

#### Purpose & Clinical Function
The `BreakGlassAlertBanner` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Prominent warning banner indicating encounter is running under emergency break-glass status. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BreakGlassAlertBannerProps {
  id: string; // Unique DOM element identifier matching 'COMP-065'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-066: TeleconsultVideoFrame
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-066`

#### Purpose & Clinical Function
The `TeleconsultVideoFrame` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. WebRTC video feed container with audio/video mute, end call, and network indicator. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TeleconsultVideoFrameProps {
  id: string; // Unique DOM element identifier matching 'COMP-066'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-067: MedicalCertificateBuilder
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-067`

#### Purpose & Clinical Function
The `MedicalCertificateBuilder` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Form generator for medical leave and fitness certificates with doctor digital seal. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MedicalCertificateBuilderProps {
  id: string; // Unique DOM element identifier matching 'COMP-067'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-068: ClinicalSignoffModal
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-068`

#### Purpose & Clinical Function
The `ClinicalSignoffModal` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Encounter completion dialog displaying final summary and PIN authorization prompt. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicalSignoffModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-068'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-069: ReferralQuickTrigger
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-069`

#### Purpose & Clinical Function
The `ReferralQuickTrigger` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Fast-action referral button linking consultation directly to 108 or hospital transfer. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReferralQuickTriggerProps {
  id: string; // Unique DOM element identifier matching 'COMP-069'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-070: VoiceToTextButton
**Category:** Clinical & Consultation | **Component Identifier:** `COMP-070`

#### Purpose & Clinical Function
The `VoiceToTextButton` component operates as a primary UI primitive within the Clinical & Consultation functional boundary. Microphone button activating client-side Web Speech API for Kannada clinical dictation. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Clinical & Consultation` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VoiceToTextButtonProps {
  id: string; // Unique DOM element identifier matching 'COMP-070'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-071: PrescriptionItemRow
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-071`

#### Purpose & Clinical Function
The `PrescriptionItemRow` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Single medication row: medicine name, dosage, frequency, food relation, and duration. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrescriptionItemRowProps {
  id: string; // Unique DOM element identifier matching 'COMP-071'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-072: FrequencySelectorGroup
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-072`

#### Purpose & Clinical Function
The `FrequencySelectorGroup` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Button group for standard clinical frequencies (1-0-1, 1-1-1, 0-0-1, SOS, STAT). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FrequencySelectorGroupProps {
  id: string; // Unique DOM element identifier matching 'COMP-072'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-073: FoodRelationToggle
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-073`

#### Purpose & Clinical Function
The `FoodRelationToggle` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Icon toggle for Before Food (ಊಟಕ್ಕೆ ಮುಂಚೆ) and After Food (ಊಟದ ನಂತರ). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FoodRelationToggleProps {
  id: string; // Unique DOM element identifier matching 'COMP-073'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-074: DosageCalculator
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-074`

#### Purpose & Clinical Function
The `DosageCalculator` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Pediatric weight-based liquid dosage calculator (mg/kg/day to ml per dose). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DosageCalculatorProps {
  id: string; // Unique DOM element identifier matching 'COMP-074'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-075: DrugInteractionAlertCard
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-075`

#### Purpose & Clinical Function
The `DrugInteractionAlertCard` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Card detailing clinical severity of detected drug-drug interaction with override reasons. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DrugInteractionAlertCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-075'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-076: StockAvailabilityPill
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-076`

#### Purpose & Clinical Function
The `StockAvailabilityPill` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Color badge indicating dispensary stock: In-Stock (Green), Low (Orange), Stockout (Red). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockAvailabilityPillProps {
  id: string; // Unique DOM element identifier matching 'COMP-076'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-077: BatchNumberBadge
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-077`

#### Purpose & Clinical Function
The `BatchNumberBadge` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Label showing assigned medicine batch number and expiry date based on FEFO logic. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BatchNumberBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-077'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-078: DispensingQuantityStepper
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-078`

#### Purpose & Clinical Function
The `DispensingQuantityStepper` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Validated counter ensuring dispensed quantity does not exceed prescribed or batch quantity. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DispensingQuantityStepperProps {
  id: string; // Unique DOM element identifier matching 'COMP-078'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-079: BarcodeScanMatcher
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-079`

#### Purpose & Clinical Function
The `BarcodeScanMatcher` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Interactive scanner matching physical barcode against electronic prescription line item. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BarcodeScanMatcherProps {
  id: string; // Unique DOM element identifier matching 'COMP-079'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-080: MedicationCounselingChecklist
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-080`

#### Purpose & Clinical Function
The `MedicationCounselingChecklist` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Interactive checklist verifying patient received verbal instructions on dosage and side effects. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MedicationCounselingChecklistProps {
  id: string; // Unique DOM element identifier matching 'COMP-080'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-081: PrescriptionPrintLayout
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-081`

#### Purpose & Clinical Function
The `PrescriptionPrintLayout` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Print-optimized DOM structure formatting prescription for A4 or thermal printer. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrescriptionPrintLayoutProps {
  id: string; // Unique DOM element identifier matching 'COMP-081'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-082: SubstituteDrugModal
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-082`

#### Purpose & Clinical Function
The `SubstituteDrugModal` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Pharmacist substitution dialog suggesting bio-equivalent in-stock generic molecules. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SubstituteDrugModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-082'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-083: PartialDispenseBanner
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-083`

#### Purpose & Clinical Function
The `PartialDispenseBanner` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Warning notice detailing remaining un-dispensed medication balance. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PartialDispenseBannerProps {
  id: string; // Unique DOM element identifier matching 'COMP-083'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-084: RefillApprovalCard
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-084`

#### Purpose & Clinical Function
The `RefillApprovalCard` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Chronic NCD 30-day medication refill review card with remaining allowed refills. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RefillApprovalCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-084'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-085: ControlledDrugVerification
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-085`

#### Purpose & Clinical Function
The `ControlledDrugVerification` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Dual-signature prompt requiring pharmacist and doctor authentication before dispense. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ControlledDrugVerificationProps {
  id: string; // Unique DOM element identifier matching 'COMP-085'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-086: FormularySearchInput
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-086`

#### Purpose & Clinical Function
The `FormularySearchInput` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Fast filter input searching through clinic 52-essential-drug list. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FormularySearchInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-086'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-087: PrescriptionHistoryTable
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-087`

#### Purpose & Clinical Function
The `PrescriptionHistoryTable` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Table listing past prescriptions with quick 'Re-order Same Regimen' action. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrescriptionHistoryTableProps {
  id: string; // Unique DOM element identifier matching 'COMP-087'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-088: MedicationLabelPreview
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-088`

#### Purpose & Clinical Function
The `MedicationLabelPreview` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Preview widget showing bilingual patient instructions as they will appear on strip sticker. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MedicationLabelPreviewProps {
  id: string; // Unique DOM element identifier matching 'COMP-088'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-089: StockExpiryWarningCard
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-089`

#### Purpose & Clinical Function
The `StockExpiryWarningCard` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Alert card highlighting batches approaching expiration within 30/60/90 days. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockExpiryWarningCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-089'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-090: PharmacyReconciliationRow
**Category:** Prescription & Pharmacy | **Component Identifier:** `COMP-090`

#### Purpose & Clinical Function
The `PharmacyReconciliationRow` component operates as a primary UI primitive within the Prescription & Pharmacy functional boundary. Row comparing system calculated stock against physical count with variance display. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Prescription & Pharmacy` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PharmacyReconciliationRowProps {
  id: string; // Unique DOM element identifier matching 'COMP-090'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-091: OPDTokenTicket
**Category:** Queue & Triage | **Component Identifier:** `COMP-091`

#### Purpose & Clinical Function
The `OPDTokenTicket` component operates as a primary UI primitive within the Queue & Triage functional boundary. Thermal ticket layout displaying token number, date, department, and barcode. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface OPDTokenTicketProps {
  id: string; // Unique DOM element identifier matching 'COMP-091'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-092: QueuePositionCard
**Category:** Queue & Triage | **Component Identifier:** `COMP-092`

#### Purpose & Clinical Function
The `QueuePositionCard` component operates as a primary UI primitive within the Queue & Triage functional boundary. Widget indicating current position in line and estimated wait time in minutes. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QueuePositionCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-092'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-093: PublicQueueBoard
**Category:** Queue & Triage | **Component Identifier:** `COMP-093`

#### Purpose & Clinical Function
The `PublicQueueBoard` component operates as a primary UI primitive within the Queue & Triage functional boundary. High-contrast public TV display board showing active token numbers by doctor cabin. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PublicQueueBoardProps {
  id: string; // Unique DOM element identifier matching 'COMP-093'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-094: AudioAnnouncementTrigger
**Category:** Queue & Triage | **Component Identifier:** `COMP-094`

#### Purpose & Clinical Function
The `AudioAnnouncementTrigger` component operates as a primary UI primitive within the Queue & Triage functional boundary. Audio speech synthesizer calling patient token in Kannada and English. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AudioAnnouncementTriggerProps {
  id: string; // Unique DOM element identifier matching 'COMP-094'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-095: PatientCallButton
**Category:** Queue & Triage | **Component Identifier:** `COMP-095`

#### Purpose & Clinical Function
The `PatientCallButton` component operates as a primary UI primitive within the Queue & Triage functional boundary. Doctor console button to advance queue, call next patient, or mark as no-show. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PatientCallButtonProps {
  id: string; // Unique DOM element identifier matching 'COMP-095'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-096: PriorityQueueBadge
**Category:** Queue & Triage | **Component Identifier:** `COMP-096`

#### Purpose & Clinical Function
The `PriorityQueueBadge` component operates as a primary UI primitive within the Queue & Triage functional boundary. Badge designating Emergency (Red), Senior (Orange), Antenatal (Purple), or Normal (Blue). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PriorityQueueBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-096'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-097: TriageVitalsCard
**Category:** Queue & Triage | **Component Identifier:** `COMP-097`

#### Purpose & Clinical Function
The `TriageVitalsCard` component operates as a primary UI primitive within the Queue & Triage functional boundary. Compact card summarizing intake vitals for quick doctor review before exam. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TriageVitalsCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-097'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-098: BloodPressureDial
**Category:** Queue & Triage | **Component Identifier:** `COMP-098`

#### Purpose & Clinical Function
The `BloodPressureDial` component operates as a primary UI primitive within the Queue & Triage functional boundary. Gauge visualization indicating normal, pre-hypertension, or Stage 1/2 hypertension. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BloodPressureDialProps {
  id: string; // Unique DOM element identifier matching 'COMP-098'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-099: OxygenSaturationIndicator
**Category:** Queue & Triage | **Component Identifier:** `COMP-099`

#### Purpose & Clinical Function
The `OxygenSaturationIndicator` component operates as a primary UI primitive within the Queue & Triage functional boundary. SpO2 gauge with immediate hypoxia alarm trigger below 94%. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface OxygenSaturationIndicatorProps {
  id: string; // Unique DOM element identifier matching 'COMP-099'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-100: BloodGlucoseBadge
**Category:** Queue & Triage | **Component Identifier:** `COMP-100`

#### Purpose & Clinical Function
The `BloodGlucoseBadge` component operates as a primary UI primitive within the Queue & Triage functional boundary. Color-coded glucose reading badge (Normal, Impaired, Severe Hyperglycemia). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BloodGlucoseBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-100'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-101: QueueReassignmentModal
**Category:** Queue & Triage | **Component Identifier:** `COMP-101`

#### Purpose & Clinical Function
The `QueueReassignmentModal` component operates as a primary UI primitive within the Queue & Triage functional boundary. Supervisor dialog to transfer patient between doctor cabins during unexpected delay. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QueueReassignmentModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-101'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-102: ExpressQueueFilter
**Category:** Queue & Triage | **Component Identifier:** `COMP-102`

#### Purpose & Clinical Function
The `ExpressQueueFilter` component operates as a primary UI primitive within the Queue & Triage functional boundary. Filter tab isolating priority demographics for fast triage intake. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ExpressQueueFilterProps {
  id: string; // Unique DOM element identifier matching 'COMP-102'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-103: NoShowResolutionModal
**Category:** Queue & Triage | **Component Identifier:** `COMP-103`

#### Purpose & Clinical Function
The `NoShowResolutionModal` component operates as a primary UI primitive within the Queue & Triage functional boundary. Handling absent patients: recall, delay 3 positions, or cancel token. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NoShowResolutionModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-103'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-104: TriageQueueTable
**Category:** Queue & Triage | **Component Identifier:** `COMP-104`

#### Purpose & Clinical Function
The `TriageQueueTable` component operates as a primary UI primitive within the Queue & Triage functional boundary. Staff nurse table displaying awaiting triage patients with elapsed waiting time. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TriageQueueTableProps {
  id: string; // Unique DOM element identifier matching 'COMP-104'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-105: QueueThroughputGauge
**Category:** Queue & Triage | **Component Identifier:** `COMP-105`

#### Purpose & Clinical Function
The `QueueThroughputGauge` component operates as a primary UI primitive within the Queue & Triage functional boundary. Speedometer gauge showing hourly citizen intake rate vs target throughput. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Queue & Triage` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QueueThroughputGaugeProps {
  id: string; // Unique DOM element identifier matching 'COMP-105'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-106: LabOrderRequisitionCard
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-106`

#### Purpose & Clinical Function
The `LabOrderRequisitionCard` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Doctor order card specifying required diagnostic tests, clinical indication, and fasting state. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabOrderRequisitionCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-106'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-107: SpecimenCollectionRow
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-107`

#### Purpose & Clinical Function
The `SpecimenCollectionRow` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Row recording phlebotomy blood draw or urine sample receipt with vial barcode. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SpecimenCollectionRowProps {
  id: string; // Unique DOM element identifier matching 'COMP-107'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-108: VialBarcodeLabel
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-108`

#### Purpose & Clinical Function
The `VialBarcodeLabel` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. 25mm x 50mm thermal barcode label for blood collection tubes. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VialBarcodeLabelProps {
  id: string; // Unique DOM element identifier matching 'COMP-108'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-109: RapidTestResultInput
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-109`

#### Purpose & Clinical Function
The `RapidTestResultInput` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Radio selector for qualitative rapid POC tests (Positive, Negative, Inconclusive). It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RapidTestResultInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-109'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-110: HematologyResultGrid
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-110`

#### Purpose & Clinical Function
The `HematologyResultGrid` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Grid for complete blood count parameters with low/normal/high reference flags. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface HematologyResultGridProps {
  id: string; // Unique DOM element identifier matching 'COMP-110'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-111: CriticalLabPanicBanner
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-111`

#### Purpose & Clinical Function
The `CriticalLabPanicBanner` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Flashing alert banner displayed when lab result falls into critical panic range. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CriticalLabPanicBannerProps {
  id: string; // Unique DOM element identifier matching 'COMP-111'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-112: LabReportPrintLayout
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-112`

#### Purpose & Clinical Function
The `LabReportPrintLayout` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Bilingual A4 diagnostic report format with technician and doctor sign-off. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabReportPrintLayoutProps {
  id: string; // Unique DOM element identifier matching 'COMP-112'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-113: AnalyzerConnectionStatus
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-113`

#### Purpose & Clinical Function
The `AnalyzerConnectionStatus` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Badge indicating USB/Serial connectivity status to automated hematology analyzer. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AnalyzerConnectionStatusProps {
  id: string; // Unique DOM element identifier matching 'COMP-113'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-114: SpecimenRejectionModal
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-114`

#### Purpose & Clinical Function
The `SpecimenRejectionModal` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Logging hemolyzed or clotted samples with mandatory request for re-draw. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SpecimenRejectionModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-114'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-115: ReagentLotExpiryBadge
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-115`

#### Purpose & Clinical Function
The `ReagentLotExpiryBadge` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Tracking test kit lot numbers, open-vial expiration, and quality control status. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReagentLotExpiryBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-115'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-116: ExternalLabReferralCard
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-116`

#### Purpose & Clinical Function
The `ExternalLabReferralCard` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Packing manifest for samples transported to central municipal referral lab. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ExternalLabReferralCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-116'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-117: LabWorksheetView
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-117`

#### Purpose & Clinical Function
The `LabWorksheetView` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Batch worksheet enabling technician to record results for multiple patients concurrently. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabWorksheetViewProps {
  id: string; // Unique DOM element identifier matching 'COMP-117'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-118: UrineAnalysisGrid
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-118`

#### Purpose & Clinical Function
The `UrineAnalysisGrid` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Dipstick grid for protein, glucose, ketones, urobilinogen, and leukocyte esterase. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface UrineAnalysisGridProps {
  id: string; // Unique DOM element identifier matching 'COMP-118'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-119: MicroscopyResultForm
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-119`

#### Purpose & Clinical Function
The `MicroscopyResultForm` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Free-text and structured findings form for stool, urine, and sputum smear exams. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MicroscopyResultFormProps {
  id: string; // Unique DOM element identifier matching 'COMP-119'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-120: LabTurnaroundTimeBadge
**Category:** Diagnostics & Lab | **Component Identifier:** `COMP-120`

#### Purpose & Clinical Function
The `LabTurnaroundTimeBadge` component operates as a primary UI primitive within the Diagnostics & Lab functional boundary. Timer badge showing elapsed time from sample collection to authorized result. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Diagnostics & Lab` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabTurnaroundTimeBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-120'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-121: StockLevelIndicator
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-121`

#### Purpose & Clinical Function
The `StockLevelIndicator` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Bar indicator displaying current stock percentage against minimum reorder point. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockLevelIndicatorProps {
  id: string; // Unique DOM element identifier matching 'COMP-121'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-122: ReorderPointAlert
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-122`

#### Purpose & Clinical Function
The `ReorderPointAlert` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Warning card indicating item has fallen below 7-day safety buffer threshold. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReorderPointAlertProps {
  id: string; // Unique DOM element identifier matching 'COMP-122'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-123: TemperatureLogGraph
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-123`

#### Purpose & Clinical Function
The `TemperatureLogGraph` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Interactive line chart plotting refrigerator telemetry with upper/lower excursion lines. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TemperatureLogGraphProps {
  id: string; // Unique DOM element identifier matching 'COMP-123'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-124: ColdChainBreachModal
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-124`

#### Purpose & Clinical Function
The `ColdChainBreachModal` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Urgent alert form recording temperature breach duration and vaccine viability check. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ColdChainBreachModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-124'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-125: GoodsReceiptVerification
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-125`

#### Purpose & Clinical Function
The `GoodsReceiptVerification` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Checklist matching delivery invoice against physical boxes from central depot. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface GoodsReceiptVerificationProps {
  id: string; // Unique DOM element identifier matching 'COMP-125'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-126: StockTransferCard
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-126`

#### Purpose & Clinical Function
The `StockTransferCard` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Inter-clinic transfer manifest detailing batch, quantity, and destination clinic. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockTransferCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-126'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-127: QuarantineActionDialog
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-127`

#### Purpose & Clinical Function
The `QuarantineActionDialog` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Securing expired, damaged, or recalled stock with photographic evidence upload. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QuarantineActionDialogProps {
  id: string; // Unique DOM element identifier matching 'COMP-127'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-128: PhysicalStocktakeRow
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-128`

#### Purpose & Clinical Function
The `PhysicalStocktakeRow` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Audit worksheet row for recording physical shelf count vs software ledger. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PhysicalStocktakeRowProps {
  id: string; // Unique DOM element identifier matching 'COMP-128'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-129: VaccineVialMonitorChip
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-129`

#### Purpose & Clinical Function
The `VaccineVialMonitorChip` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. VVM Stage 1 to 4 selector determining whether vaccine can be administered. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VaccineVialMonitorChipProps {
  id: string; // Unique DOM element identifier matching 'COMP-129'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-130: DailyConsumptionCard
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-130`

#### Purpose & Clinical Function
The `DailyConsumptionCard` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Summary of items deducted through dispensing during active clinic day. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DailyConsumptionCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-130'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-131: DepotIndentBuilder
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-131`

#### Purpose & Clinical Function
The `DepotIndentBuilder` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Automated monthly indent generator calculating suggested order based on consumption. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DepotIndentBuilderProps {
  id: string; // Unique DOM element identifier matching 'COMP-131'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-132: BatchTraceabilityViewer
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-132`

#### Purpose & Clinical Function
The `BatchTraceabilityViewer` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Audit trail showing complete lifecycle of a batch from receipt to citizen dispensation. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BatchTraceabilityViewerProps {
  id: string; // Unique DOM element identifier matching 'COMP-132'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-133: BiomedicalWasteLogForm
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-133`

#### Purpose & Clinical Function
The `BiomedicalWasteLogForm` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Color-coded waste bin weighing entry (Yellow, Red, Blue, White) before vendor pickup. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BiomedicalWasteLogFormProps {
  id: string; // Unique DOM element identifier matching 'COMP-133'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-134: EmergencyStockEmergencyButton
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-134`

#### Purpose & Clinical Function
The `EmergencyStockEmergencyButton` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Fast SOS button alerting Zonal Pharmacist to impending stockout of lifesaving drugs. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface EmergencyStockEmergencyButtonProps {
  id: string; // Unique DOM element identifier matching 'COMP-134'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-135: InventoryValuationWidget
**Category:** Inventory & Logistics | **Component Identifier:** `COMP-135`

#### Purpose & Clinical Function
The `InventoryValuationWidget` component operates as a primary UI primitive within the Inventory & Logistics functional boundary. Financial summary of total medicines held on premises at government procurement rates. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Inventory & Logistics` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface InventoryValuationWidgetProps {
  id: string; // Unique DOM element identifier matching 'COMP-135'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-136: NetworkConnectivityBanner
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-136`

#### Purpose & Clinical Function
The `NetworkConnectivityBanner` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Floating banner alerting user of Online, Degraded (2G/3G), or Offline network state. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NetworkConnectivityBannerProps {
  id: string; // Unique DOM element identifier matching 'COMP-136'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-137: SyncQueueDrawer
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-137`

#### Purpose & Clinical Function
The `SyncQueueDrawer` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Slide-over drawer displaying pending local mutations waiting for network reconnection. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SyncQueueDrawerProps {
  id: string; // Unique DOM element identifier matching 'COMP-137'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-138: ConflictDiffModal
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-138`

#### Purpose & Clinical Function
The `ConflictDiffModal` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Side-by-side comparison modal allowing clinician to resolve conflicting edits. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ConflictDiffModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-138'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-139: LocalDiskQuotaMeter
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-139`

#### Purpose & Clinical Function
The `LocalDiskQuotaMeter` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Storage meter displaying IndexedDB and SQLite disk consumption on clinic device. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LocalDiskQuotaMeterProps {
  id: string; // Unique DOM element identifier matching 'COMP-139'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-140: OfflineLoginIndicator
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-140`

#### Purpose & Clinical Function
The `OfflineLoginIndicator` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Badge showing user is authenticated via local SQLite cached credentials. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface OfflineLoginIndicatorProps {
  id: string; // Unique DOM element identifier matching 'COMP-140'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-141: ManualSyncTriggerButton
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-141`

#### Purpose & Clinical Function
The `ManualSyncTriggerButton` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Button triggering immediate cryptographic synchronization handshake with central cloud. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ManualSyncTriggerButtonProps {
  id: string; // Unique DOM element identifier matching 'COMP-141'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-142: PeerSyncDiscoveryBadge
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-142`

#### Purpose & Clinical Function
The `PeerSyncDiscoveryBadge` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Indicator showing tablet is connected to local clinic mini-PC via LAN / mDNS. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PeerSyncDiscoveryBadgeProps {
  id: string; // Unique DOM element identifier matching 'COMP-142'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-143: SyncErrorAlertCard
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-143`

#### Purpose & Clinical Function
The `SyncErrorAlertCard` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Notification card explaining rejected sync mutation with automated recovery instructions. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SyncErrorAlertCardProps {
  id: string; // Unique DOM element identifier matching 'COMP-143'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-144: UnsavedChangesGuardModal
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-144`

#### Purpose & Clinical Function
The `UnsavedChangesGuardModal` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Navigation blocker preventing accidental exit from form before local persistence. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface UnsavedChangesGuardModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-144'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-145: DatabaseCompactButton
**Category:** Offline & Synchronization | **Component Identifier:** `COMP-145`

#### Purpose & Clinical Function
The `DatabaseCompactButton` component operates as a primary UI primitive within the Offline & Synchronization functional boundary. Administrative maintenance button triggering local SQLite VACUUM and index rebuild. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Offline & Synchronization` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DatabaseCompactButtonProps {
  id: string; // Unique DOM element identifier matching 'COMP-145'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-146: PrintPreviewModal
**Category:** Printing & Export | **Component Identifier:** `COMP-146`

#### Purpose & Clinical Function
The `PrintPreviewModal` component operates as a primary UI primitive within the Printing & Export functional boundary. Modal rendering exact print page layout before sending to local hardware printer. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrintPreviewModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-146'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-147: ThermalPrinterSelector
**Category:** Printing & Export | **Component Identifier:** `COMP-147`

#### Purpose & Clinical Function
The `ThermalPrinterSelector` component operates as a primary UI primitive within the Printing & Export functional boundary. Settings dropdown selecting network or USB ESC/POS 80mm thermal receipt printer. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ThermalPrinterSelectorProps {
  id: string; // Unique DOM element identifier matching 'COMP-147'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-148: PDFExportProgressModal
**Category:** Printing & Export | **Component Identifier:** `COMP-148`

#### Purpose & Clinical Function
The `PDFExportProgressModal` component operates as a primary UI primitive within the Printing & Export functional boundary. Progress dialog generating client-side encrypted PDF for citizen records. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PDFExportProgressModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-148'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-149: KannadaPrintFontInjector
**Category:** Printing & Export | **Component Identifier:** `COMP-149`

#### Purpose & Clinical Function
The `KannadaPrintFontInjector` component operates as a primary UI primitive within the Printing & Export functional boundary. CSS print engine injecting embedded Kannada Noto Serif fonts for clean thermal print. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface KannadaPrintFontInjectorProps {
  id: string; // Unique DOM element identifier matching 'COMP-149'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-150: BarcodePrintGenerator
**Category:** Printing & Export | **Component Identifier:** `COMP-150`

#### Purpose & Clinical Function
The `BarcodePrintGenerator` component operates as a primary UI primitive within the Printing & Export functional boundary. Client-side SVG Code-128 barcode generator for patient wristbands and vials. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BarcodePrintGeneratorProps {
  id: string; // Unique DOM element identifier matching 'COMP-150'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-151: ReprintAuthorizationModal
**Category:** Printing & Export | **Component Identifier:** `COMP-151`

#### Purpose & Clinical Function
The `ReprintAuthorizationModal` component operates as a primary UI primitive within the Printing & Export functional boundary. Supervisor PIN prompt required before reprinting prescription or OPD token. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReprintAuthorizationModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-151'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-152: PrintAuditNotifier
**Category:** Printing & Export | **Component Identifier:** `COMP-152`

#### Purpose & Clinical Function
The `PrintAuditNotifier` component operates as a primary UI primitive within the Printing & Export functional boundary. Silent background hook recording print event and document hash into WORM audit ledger. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Printing & Export` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrintAuditNotifierProps {
  id: string; // Unique DOM element identifier matching 'COMP-152'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-153: SkipToContentLink
**Category:** Accessibility & Security | **Component Identifier:** `COMP-153`

#### Purpose & Clinical Function
The `SkipToContentLink` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Hidden accessible anchor allowing keyboard users to bypass header navigation. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SkipToContentLinkProps {
  id: string; // Unique DOM element identifier matching 'COMP-153'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-154: ScreenReaderLiveRegion
**Category:** Accessibility & Security | **Component Identifier:** `COMP-154`

#### Purpose & Clinical Function
The `ScreenReaderLiveRegion` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Aria-live polite and assertive announcer for dynamic state updates. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ScreenReaderLiveRegionProps {
  id: string; // Unique DOM element identifier matching 'COMP-154'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-155: SessionInactivityWarningModal
**Category:** Accessibility & Security | **Component Identifier:** `COMP-155`

#### Purpose & Clinical Function
The `SessionInactivityWarningModal` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Countdown modal warning clinician of session logout due to 15 minutes of inactivity. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SessionInactivityWarningModalProps {
  id: string; // Unique DOM element identifier matching 'COMP-155'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-156: BreakGlassConfirmDialog
**Category:** Accessibility & Security | **Component Identifier:** `COMP-156`

#### Purpose & Clinical Function
The `BreakGlassConfirmDialog` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Dual-confirmation dialog capturing clinical justification for emergency access. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BreakGlassConfirmDialogProps {
  id: string; // Unique DOM element identifier matching 'COMP-156'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-157: PinPadInput
**Category:** Accessibility & Security | **Component Identifier:** `COMP-157`

#### Purpose & Clinical Function
The `PinPadInput` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Touchscreen on-screen numeric keypad for quick 4-digit PIN authentication. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PinPadInputProps {
  id: string; // Unique DOM element identifier matching 'COMP-157'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-158: PrivacyMaskToggle
**Category:** Accessibility & Security | **Component Identifier:** `COMP-158`

#### Purpose & Clinical Function
The `PrivacyMaskToggle` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Eye icon button allowing clinician to blur sensitive HIV/mental health notes on screen. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrivacyMaskToggleProps {
  id: string; // Unique DOM element identifier matching 'COMP-158'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-159: HighContrastModeToggle
**Category:** Accessibility & Security | **Component Identifier:** `COMP-159`

#### Purpose & Clinical Function
The `HighContrastModeToggle` component operates as a primary UI primitive within the Accessibility & Security functional boundary. Header button switching UI to 7:1 contrast ratio for low-vision clinic operators. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface HighContrastModeToggleProps {
  id: string; // Unique DOM element identifier matching 'COMP-159'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

### COMP-160: KannadaLanguageToggle
**Category:** Accessibility & Security | **Component Identifier:** `COMP-160`

#### Purpose & Clinical Function
The `KannadaLanguageToggle` component operates as a primary UI primitive within the Accessibility & Security functional boundary. One-click toggle switching all application text between Kannada (ಕನ್ನಡ) and English. It is specifically optimized to meet BBMP healthcare operational standards, ensuring instantaneous perceptual clarity for clinic personnel under high outpatient loads.

#### Visual & Interactive States
- **Default (Resting):** Adheres to `Accessibility & Security` base elevation and border radius (6px). Border color matches `COLOR_TOKENS.neutrals.border` with background `COLOR_TOKENS.neutrals.surface`.
- **Hover State:** Elevation smoothly transitions to `shadow-md` (0 4px 6px -1px rgb(0 0 0 / 0.1)) with border highlighting in `COLOR_TOKENS.brand.primary`.
- **Active / Pressed:** Visual depression effect (0.98 scale transform) with border shifting to `COLOR_TOKENS.brand.primaryActive`.
- **Keyboard Focus:** High-visibility 3px outer ring in `#005A9C` with 2px white offset (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Disabled State:** Opacity reduced to 0.45, `cursor: not-allowed`, pointer events suppressed, ARIA attribute `aria-disabled='true'`.
- **Error / Validation Failure:** Outline switches to `COLOR_TOKENS.clinical.emergencyRed` (2px solid) with inline SVG warning icon and `aria-invalid='true'`.
- **Offline / Degraded Mode:** Visual fallback state rendering localized warning badge when mutations must be held in client-side queue.

#### Accessibility (WCAG 2.1 AA) & Keyboard Contract
- **Semantic Role:** Appropriate HTML5 element with explicit ARIA role (`role='region'`, `role='button'`, or `role='form'`).
- **Tab Order:** Integrated into natural sequential document tabindex (`tabindex='0'`), supporting full operational workflow without pointing devices.
- **Keyboard Triggers:** Activated via `Enter` or `Space` key; dismissible via `Escape` key where applicable.
- **Screen Reader Announcement:** Integrated with `COMP-154: ScreenReaderLiveRegion` to announce dynamic state changes in Kannada and English.

#### Localization & Kannada Typography Behavior
- **Font Family:** Inherits `TYPOGRAPHY_TOKENS.fontFamily.kannadaPrimary` when Kannada locale is active.
- **Horizontal Expansion:** Container enforces minimum 25% horizontal padding buffer to accommodate Kannada syllable expansion without word wrapping or truncation.
- **Line Height Buffer:** Standard line-height clamped at 1.6 (`TYPOGRAPHY_TOKENS.lineHeight.kannada`) preventing clipping of subscripts and superscripts.

#### Documentation-Only TypeScript Interface
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface KannadaLanguageToggleProps {
  id: string; // Unique DOM element identifier matching 'COMP-160'
  className?: string; // Optional styling overrides
  locale?: 'kn-IN' | 'en-IN'; // Active bilingual locale
  isDisabled?: boolean; // Disables user interaction
  isOffline?: boolean; // Visual indicator for edge disconnected state
  onAction?: (event: unknown) => void; // Event dispatcher
}
```

---

## 6. Design System Anti-Patterns & Visual QA Rules
1. **No Ad-Hoc Colors:** Developers MUST NOT declare arbitrary HEX or HSL colors in component styles. All visual styling must derive strictly from `COLOR_TOKENS`.
2. **No Text Truncation Without Tooltip:** Medical names, diagnoses, and drug dosages must never be clipped with `text-overflow: ellipsis` without an accessible tooltip or disclosure button.
3. **No Mouse-Only Actions:** Every clinical CTA, form field, and table row expansion must be fully navigable and executable via keyboard alone.
4. **No Unannotated Code Blocks:** All illustrative code examples must maintain strict `-- DOCUMENTATION-ONLY` or `// DOCUMENTATION-ONLY` annotations.
5. **Strict Bilingual Testing:** Every component must be visually verified under both English and Kannada rendering to eliminate layout breaks caused by font metric variance.
