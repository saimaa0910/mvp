# Namma Clinic Reusable Component Catalog Specification

## 1. Executive Summary & Component Architecture
This document defines the complete canonical registry of all **160 planned reusable frontend components** (`COMP-001` through `COMP-160`) across 11 functional domains for the Namma Clinic Platform. Each component is engineered as an isolated, accessible, typed, and localized primitive adhering to strict clinical safety and visual consistency standards.

## 2. Global Component Master Index
| Component ID | Component Name | Functional Category | Primary Operational Scope |
| :--- | :--- | :--- | :--- |
| `COMP-001` | AppShell | Layout & Navigation | Master application container with responsive header, collapsible sidebar, and offline banner |
| `COMP-002` | ClinicHeader | Layout & Navigation | Top navigation bar showing clinic name, ward code, active doctor name, sync badge, and language toggle |
| `COMP-003` | RoleSidebar | Layout & Navigation | Dynamic sidebar rendering only permitted navigation routes based on active user role |
| `COMP-004` | BreadcrumbNav | Layout & Navigation | Hierarchical navigation trail with deep-link support and keyboard tab focus |
| `COMP-005` | TabBar | Layout & Navigation | Multi-tab sub-navigation for clinical encounters and patient longitudinal record sections |
| `COMP-006` | SplitPaneLayout | Layout & Navigation | Dual-pane responsive layout for simultaneous patient record view and consultation notes entry |
| `COMP-007` | PageContainer | Layout & Navigation | Standard content wrapper enforcing responsive margins, maximum width, and padding |
| `COMP-008` | ActionToolbar | Layout & Navigation | Sticky action bar with primary CTA, secondary actions, and cancel/back buttons |
| `COMP-009` | MobileBottomNav | Layout & Navigation | Bottom icon bar optimized for tablet and handheld mobile screens |
| `COMP-010` | DrawerContainer | Layout & Navigation | Slide-out side drawer for quick patient summary, sync queue, or notifications |
| `COMP-011` | CollapsibleSection | Layout & Navigation | Accordion card with smooth expansion toggle and ARIA expanded state |
| `COMP-012` | CardSurface | Layout & Navigation | Elevated visual card container with standardized borders, radius, and shadows |
| `COMP-013` | ModalContainer | Layout & Navigation | Accessible modal dialog overlay with focus trap, backdrop blur, and escape key listener |
| `COMP-014` | KeyboardShortcutGuide | Layout & Navigation | Floating cheat sheet displaying fast-action keyboard shortcuts for clinical workflows |
| `COMP-015` | FooterStatusStrip | Layout & Navigation | Bottom status strip displaying local SQLite sync state, memory usage, and software version |
| `COMP-016` | StatusBadge | Data Display & Feedback | Color-coded status chip for visit states, lab statuses, and triage urgency tiers |
| `COMP-017` | ToastNotification | Data Display & Feedback | Auto-dismissing toast alert with success, warning, error, and info styles |
| `COMP-018` | SystemAlertBanner | Data Display & Feedback | Prominent full-width alert banner for network disconnection or emergency alerts |
| `COMP-019` | EmptyStateDisplay | Data Display & Feedback | Illustrative placeholder with descriptive text and clear primary action button |
| `COMP-020` | LoadingSkeletonCard | Data Display & Feedback | Shimmering animated skeleton placeholder matching target content geometry |
| `COMP-021` | LoadingSpinner | Data Display & Feedback | Lightweight SVG circular activity indicator with accessible aria-busy announce |
| `COMP-022` | LinearProgressBar | Data Display & Feedback | Determinate and indeterminate progress bar for batch operations and sync progress |
| `COMP-023` | MetricStatCard | Data Display & Feedback | KPI stat card displaying numerical figure, trend sparkline, and percentage change |
| `COMP-024` | DataTableGrid | Data Display & Feedback | High-performance virtualized table supporting sorting, filtering, and column resize |
| `COMP-025` | PaginationControl | Data Display & Feedback | Accessible pagination toolbar with page jump, size selector, and item counts |
| `COMP-026` | ConfirmationDialog | Data Display & Feedback | Destructive action confirmation modal with explicit hazard warning and dual confirmation |
| `COMP-027` | TooltipWrapper | Data Display & Feedback | Hover and focus triggered tooltip providing micro-help in Kannada and English |
| `COMP-028` | PopoverMenu | Data Display & Feedback | Contextual action popover menu positioned dynamically next to trigger element |
| `COMP-029` | TagCloud | Data Display & Feedback | Interactive collection of chips for symptom tags, allergy labels, and diagnosis tags |
| `COMP-030` | AuditDiffViewer | Data Display & Feedback | Side-by-side visual diff component showing before-and-after state changes in records |
| `COMP-031` | TextInput | Form Controls & Inputs | Single-line text input with floating label, validation error icon, and clear button |
| `COMP-032` | MaskedPhoneInput | Form Controls & Inputs | Indian 10-digit mobile number input with +91 prefix and automatic formatting |
| `COMP-033` | AadhaarMaskedInput | Form Controls & Inputs | 12-digit national ID input with automated masking (XXXX-XXXX-1234) for privacy |
| `COMP-034` | NumberInputStepper | Form Controls & Inputs | Numeric input with increment/decrement steppers and min/max clamping |
| `COMP-035` | SearchableCombobox | Form Controls & Inputs | Autocomplete dropdown with asynchronous search, keyboard navigation, and create-new option |
| `COMP-036` | SingleSelectDropdown | Form Controls & Inputs | Standard select menu with native mobile fallback and accessible keyboard navigation |
| `COMP-037` | MultiSelectCheckboxDropdown | Form Controls & Inputs | Dropdown enabling multiple checkbox selections with selected count badges |
| `COMP-038` | DatePickerCalendar | Form Controls & Inputs | Accessible calendar popup supporting date selection with Kannada month labels |
| `COMP-039` | TimePickerControl | Form Controls & Inputs | 12/24 hour time selector with AM/PM toggle and quick-select presets |
| `COMP-040` | RadioGroupSelector | Form Controls & Inputs | Accessible radio button group with arrow key navigation and label descriptions |
| `COMP-041` | CheckboxControl | Form Controls & Inputs | Standard checkbox with custom checkmark icon, indeterminate state, and error styling |
| `COMP-042` | ToggleSwitch | Form Controls & Inputs | Binary on/off toggle switch with smooth sliding animation and high-contrast focus ring |
| `COMP-043` | TextAreaInput | Form Controls & Inputs | Multi-line text area with auto-expansion, character counter, and spellcheck toggle |
| `COMP-044` | DigitalSignaturePad | Form Controls & Inputs | HTML5 canvas signature pad for citizen consent and clinician sign-off with clear/undo |
| `COMP-045` | WebcamCaptureWidget | Form Controls & Inputs | Browser webcam interface with face guide overlay, capture snapshot, and retake controls |
| `COMP-046` | BarcodeScannerInput | Form Controls & Inputs | Hardware HID barcode scanner listener with debounce and audio beep feedback |
| `COMP-047` | FileUploadDropzone | Form Controls & Inputs | Drag-and-drop document upload area with file size validation and thumbnail preview |
| `COMP-048` | PasswordInput | Form Controls & Inputs | Secure password field with visibility toggle, strength meter, and caps-lock warning |
| `COMP-049` | FormActionFooter | Form Controls & Inputs | Standardized form button row with Submit, Reset, and Save Draft buttons |
| `COMP-050` | FieldValidationError | Form Controls & Inputs | Accessible inline error message with role='alert' and SVG warning icon |
| `COMP-051` | PatientBanner | Clinical & Consultation | Persistent patient header displaying UHID, photo, name, age/gender, allergies, and vitals |
| `COMP-052` | VitalsGridDisplay | Clinical & Consultation | Structured grid displaying current visit vitals with abnormal value highlighting |
| `COMP-053` | VitalsTrendSparkline | Clinical & Consultation | Miniature line chart showing systolic BP or blood sugar trend across past 5 visits |
| `COMP-054` | DangerScoreBadge | Clinical & Consultation | Early Warning Score (MEWS/PEWS) color-coded badge indicating clinical risk level |
| `COMP-055` | AllergyAlertChip | Clinical & Consultation | High-visibility red warning chip highlighting confirmed drug allergies on hover/click |
| `COMP-056` | DiagnosisSearchCombobox | Clinical & Consultation | Dual-search ICD-10 and SNOMED CT diagnosis selector with Kannada common terms |
| `COMP-057` | ChiefComplaintSelector | Clinical & Consultation | Interactive body map and common complaints grid for rapid symptom logging |
| `COMP-058` | ClinicalHistoryTimeline | Clinical & Consultation | Vertical timeline depicting past diagnoses, prescriptions, and lab tests chronologically |
| `COMP-059` | ConsultationTimer | Clinical & Consultation | Discreet timer tracking duration of patient encounter for clinic workflow analytics |
| `COMP-060` | PediatricPercentileCard | Clinical & Consultation | WHO child growth percentile card plotting weight-for-age and height-for-age |
| `COMP-061` | ANCEncounterCard | Clinical & Consultation | Antenatal care tracker displaying trimester, expected delivery date, and high-risk flags |
| `COMP-062` | NCDTrackingCard | Clinical & Consultation | Chronic illness management summary displaying 3-month HbA1c and BP control metrics |
| `COMP-063` | ClinicalNoteEditor | Clinical & Consultation | Rich text SOAP clinical note editor with pre-filled physical examination templates |
| `COMP-064` | DrugAllergyModal | Clinical & Consultation | Formal modal for recording new drug or food allergies with reaction severity |
| `COMP-065` | BreakGlassAlertBanner | Clinical & Consultation | Prominent warning banner indicating encounter is running under emergency break-glass status |
| `COMP-066` | TeleconsultVideoFrame | Clinical & Consultation | WebRTC video feed container with audio/video mute, end call, and network indicator |
| `COMP-067` | MedicalCertificateBuilder | Clinical & Consultation | Form generator for medical leave and fitness certificates with doctor digital seal |
| `COMP-068` | ClinicalSignoffModal | Clinical & Consultation | Encounter completion dialog displaying final summary and PIN authorization prompt |
| `COMP-069` | ReferralQuickTrigger | Clinical & Consultation | Fast-action referral button linking consultation directly to 108 or hospital transfer |
| `COMP-070` | VoiceToTextButton | Clinical & Consultation | Microphone button activating client-side Web Speech API for Kannada clinical dictation |
| `COMP-071` | PrescriptionItemRow | Prescription & Pharmacy | Single medication row: medicine name, dosage, frequency, food relation, and duration |
| `COMP-072` | FrequencySelectorGroup | Prescription & Pharmacy | Button group for standard clinical frequencies (1-0-1, 1-1-1, 0-0-1, SOS, STAT) |
| `COMP-073` | FoodRelationToggle | Prescription & Pharmacy | Icon toggle for Before Food (ಊಟಕ್ಕೆ ಮುಂಚೆ) and After Food (ಊಟದ ನಂತರ) |
| `COMP-074` | DosageCalculator | Prescription & Pharmacy | Pediatric weight-based liquid dosage calculator (mg/kg/day to ml per dose) |
| `COMP-075` | DrugInteractionAlertCard | Prescription & Pharmacy | Card detailing clinical severity of detected drug-drug interaction with override reasons |
| `COMP-076` | StockAvailabilityPill | Prescription & Pharmacy | Color badge indicating dispensary stock: In-Stock (Green), Low (Orange), Stockout (Red) |
| `COMP-077` | BatchNumberBadge | Prescription & Pharmacy | Label showing assigned medicine batch number and expiry date based on FEFO logic |
| `COMP-078` | DispensingQuantityStepper | Prescription & Pharmacy | Validated counter ensuring dispensed quantity does not exceed prescribed or batch quantity |
| `COMP-079` | BarcodeScanMatcher | Prescription & Pharmacy | Interactive scanner matching physical barcode against electronic prescription line item |
| `COMP-080` | MedicationCounselingChecklist | Prescription & Pharmacy | Interactive checklist verifying patient received verbal instructions on dosage and side effects |
| `COMP-081` | PrescriptionPrintLayout | Prescription & Pharmacy | Print-optimized DOM structure formatting prescription for A4 or thermal printer |
| `COMP-082` | SubstituteDrugModal | Prescription & Pharmacy | Pharmacist substitution dialog suggesting bio-equivalent in-stock generic molecules |
| `COMP-083` | PartialDispenseBanner | Prescription & Pharmacy | Warning notice detailing remaining un-dispensed medication balance |
| `COMP-084` | RefillApprovalCard | Prescription & Pharmacy | Chronic NCD 30-day medication refill review card with remaining allowed refills |
| `COMP-085` | ControlledDrugVerification | Prescription & Pharmacy | Dual-signature prompt requiring pharmacist and doctor authentication before dispense |
| `COMP-086` | FormularySearchInput | Prescription & Pharmacy | Fast filter input searching through clinic 52-essential-drug list |
| `COMP-087` | PrescriptionHistoryTable | Prescription & Pharmacy | Table listing past prescriptions with quick 'Re-order Same Regimen' action |
| `COMP-088` | MedicationLabelPreview | Prescription & Pharmacy | Preview widget showing bilingual patient instructions as they will appear on strip sticker |
| `COMP-089` | StockExpiryWarningCard | Prescription & Pharmacy | Alert card highlighting batches approaching expiration within 30/60/90 days |
| `COMP-090` | PharmacyReconciliationRow | Prescription & Pharmacy | Row comparing system calculated stock against physical count with variance display |
| `COMP-091` | OPDTokenTicket | Queue & Triage | Thermal ticket layout displaying token number, date, department, and barcode |
| `COMP-092` | QueuePositionCard | Queue & Triage | Widget indicating current position in line and estimated wait time in minutes |
| `COMP-093` | PublicQueueBoard | Queue & Triage | High-contrast public TV display board showing active token numbers by doctor cabin |
| `COMP-094` | AudioAnnouncementTrigger | Queue & Triage | Audio speech synthesizer calling patient token in Kannada and English |
| `COMP-095` | PatientCallButton | Queue & Triage | Doctor console button to advance queue, call next patient, or mark as no-show |
| `COMP-096` | PriorityQueueBadge | Queue & Triage | Badge designating Emergency (Red), Senior (Orange), Antenatal (Purple), or Normal (Blue) |
| `COMP-097` | TriageVitalsCard | Queue & Triage | Compact card summarizing intake vitals for quick doctor review before exam |
| `COMP-098` | BloodPressureDial | Queue & Triage | Gauge visualization indicating normal, pre-hypertension, or Stage 1/2 hypertension |
| `COMP-099` | OxygenSaturationIndicator | Queue & Triage | SpO2 gauge with immediate hypoxia alarm trigger below 94% |
| `COMP-100` | BloodGlucoseBadge | Queue & Triage | Color-coded glucose reading badge (Normal, Impaired, Severe Hyperglycemia) |
| `COMP-101` | QueueReassignmentModal | Queue & Triage | Supervisor dialog to transfer patient between doctor cabins during unexpected delay |
| `COMP-102` | ExpressQueueFilter | Queue & Triage | Filter tab isolating priority demographics for fast triage intake |
| `COMP-103` | NoShowResolutionModal | Queue & Triage | Handling absent patients: recall, delay 3 positions, or cancel token |
| `COMP-104` | TriageQueueTable | Queue & Triage | Staff nurse table displaying awaiting triage patients with elapsed waiting time |
| `COMP-105` | QueueThroughputGauge | Queue & Triage | Speedometer gauge showing hourly citizen intake rate vs target throughput |
| `COMP-106` | LabOrderRequisitionCard | Diagnostics & Lab | Doctor order card specifying required diagnostic tests, clinical indication, and fasting state |
| `COMP-107` | SpecimenCollectionRow | Diagnostics & Lab | Row recording phlebotomy blood draw or urine sample receipt with vial barcode |
| `COMP-108` | VialBarcodeLabel | Diagnostics & Lab | 25mm x 50mm thermal barcode label for blood collection tubes |
| `COMP-109` | RapidTestResultInput | Diagnostics & Lab | Radio selector for qualitative rapid POC tests (Positive, Negative, Inconclusive) |
| `COMP-110` | HematologyResultGrid | Diagnostics & Lab | Grid for complete blood count parameters with low/normal/high reference flags |
| `COMP-111` | CriticalLabPanicBanner | Diagnostics & Lab | Flashing alert banner displayed when lab result falls into critical panic range |
| `COMP-112` | LabReportPrintLayout | Diagnostics & Lab | Bilingual A4 diagnostic report format with technician and doctor sign-off |
| `COMP-113` | AnalyzerConnectionStatus | Diagnostics & Lab | Badge indicating USB/Serial connectivity status to automated hematology analyzer |
| `COMP-114` | SpecimenRejectionModal | Diagnostics & Lab | Logging hemolyzed or clotted samples with mandatory request for re-draw |
| `COMP-115` | ReagentLotExpiryBadge | Diagnostics & Lab | Tracking test kit lot numbers, open-vial expiration, and quality control status |
| `COMP-116` | ExternalLabReferralCard | Diagnostics & Lab | Packing manifest for samples transported to central municipal referral lab |
| `COMP-117` | LabWorksheetView | Diagnostics & Lab | Batch worksheet enabling technician to record results for multiple patients concurrently |
| `COMP-118` | UrineAnalysisGrid | Diagnostics & Lab | Dipstick grid for protein, glucose, ketones, urobilinogen, and leukocyte esterase |
| `COMP-119` | MicroscopyResultForm | Diagnostics & Lab | Free-text and structured findings form for stool, urine, and sputum smear exams |
| `COMP-120` | LabTurnaroundTimeBadge | Diagnostics & Lab | Timer badge showing elapsed time from sample collection to authorized result |
| `COMP-121` | StockLevelIndicator | Inventory & Logistics | Bar indicator displaying current stock percentage against minimum reorder point |
| `COMP-122` | ReorderPointAlert | Inventory & Logistics | Warning card indicating item has fallen below 7-day safety buffer threshold |
| `COMP-123` | TemperatureLogGraph | Inventory & Logistics | Interactive line chart plotting refrigerator telemetry with upper/lower excursion lines |
| `COMP-124` | ColdChainBreachModal | Inventory & Logistics | Urgent alert form recording temperature breach duration and vaccine viability check |
| `COMP-125` | GoodsReceiptVerification | Inventory & Logistics | Checklist matching delivery invoice against physical boxes from central depot |
| `COMP-126` | StockTransferCard | Inventory & Logistics | Inter-clinic transfer manifest detailing batch, quantity, and destination clinic |
| `COMP-127` | QuarantineActionDialog | Inventory & Logistics | Securing expired, damaged, or recalled stock with photographic evidence upload |
| `COMP-128` | PhysicalStocktakeRow | Inventory & Logistics | Audit worksheet row for recording physical shelf count vs software ledger |
| `COMP-129` | VaccineVialMonitorChip | Inventory & Logistics | VVM Stage 1 to 4 selector determining whether vaccine can be administered |
| `COMP-130` | DailyConsumptionCard | Inventory & Logistics | Summary of items deducted through dispensing during active clinic day |
| `COMP-131` | DepotIndentBuilder | Inventory & Logistics | Automated monthly indent generator calculating suggested order based on consumption |
| `COMP-132` | BatchTraceabilityViewer | Inventory & Logistics | Audit trail showing complete lifecycle of a batch from receipt to citizen dispensation |
| `COMP-133` | BiomedicalWasteLogForm | Inventory & Logistics | Color-coded waste bin weighing entry (Yellow, Red, Blue, White) before vendor pickup |
| `COMP-134` | EmergencyStockEmergencyButton | Inventory & Logistics | Fast SOS button alerting Zonal Pharmacist to impending stockout of lifesaving drugs |
| `COMP-135` | InventoryValuationWidget | Inventory & Logistics | Financial summary of total medicines held on premises at government procurement rates |
| `COMP-136` | NetworkConnectivityBanner | Offline & Synchronization | Floating banner alerting user of Online, Degraded (2G/3G), or Offline network state |
| `COMP-137` | SyncQueueDrawer | Offline & Synchronization | Slide-over drawer displaying pending local mutations waiting for network reconnection |
| `COMP-138` | ConflictDiffModal | Offline & Synchronization | Side-by-side comparison modal allowing clinician to resolve conflicting edits |
| `COMP-139` | LocalDiskQuotaMeter | Offline & Synchronization | Storage meter displaying IndexedDB and SQLite disk consumption on clinic device |
| `COMP-140` | OfflineLoginIndicator | Offline & Synchronization | Badge showing user is authenticated via local SQLite cached credentials |
| `COMP-141` | ManualSyncTriggerButton | Offline & Synchronization | Button triggering immediate cryptographic synchronization handshake with central cloud |
| `COMP-142` | PeerSyncDiscoveryBadge | Offline & Synchronization | Indicator showing tablet is connected to local clinic mini-PC via LAN / mDNS |
| `COMP-143` | SyncErrorAlertCard | Offline & Synchronization | Notification card explaining rejected sync mutation with automated recovery instructions |
| `COMP-144` | UnsavedChangesGuardModal | Offline & Synchronization | Navigation blocker preventing accidental exit from form before local persistence |
| `COMP-145` | DatabaseCompactButton | Offline & Synchronization | Administrative maintenance button triggering local SQLite VACUUM and index rebuild |
| `COMP-146` | PrintPreviewModal | Printing & Export | Modal rendering exact print page layout before sending to local hardware printer |
| `COMP-147` | ThermalPrinterSelector | Printing & Export | Settings dropdown selecting network or USB ESC/POS 80mm thermal receipt printer |
| `COMP-148` | PDFExportProgressModal | Printing & Export | Progress dialog generating client-side encrypted PDF for citizen records |
| `COMP-149` | KannadaPrintFontInjector | Printing & Export | CSS print engine injecting embedded Kannada Noto Serif fonts for clean thermal print |
| `COMP-150` | BarcodePrintGenerator | Printing & Export | Client-side SVG Code-128 barcode generator for patient wristbands and vials |
| `COMP-151` | ReprintAuthorizationModal | Printing & Export | Supervisor PIN prompt required before reprinting prescription or OPD token |
| `COMP-152` | PrintAuditNotifier | Printing & Export | Silent background hook recording print event and document hash into WORM audit ledger |
| `COMP-153` | SkipToContentLink | Accessibility & Security | Hidden accessible anchor allowing keyboard users to bypass header navigation |
| `COMP-154` | ScreenReaderLiveRegion | Accessibility & Security | Aria-live polite and assertive announcer for dynamic state updates |
| `COMP-155` | SessionInactivityWarningModal | Accessibility & Security | Countdown modal warning clinician of session logout due to 15 minutes of inactivity |
| `COMP-156` | BreakGlassConfirmDialog | Accessibility & Security | Dual-confirmation dialog capturing clinical justification for emergency access |
| `COMP-157` | PinPadInput | Accessibility & Security | Touchscreen on-screen numeric keypad for quick 4-digit PIN authentication |
| `COMP-158` | PrivacyMaskToggle | Accessibility & Security | Eye icon button allowing clinician to blur sensitive HIV/mental health notes on screen |
| `COMP-159` | HighContrastModeToggle | Accessibility & Security | Header button switching UI to 7:1 contrast ratio for low-vision clinic operators |
| `COMP-160` | KannadaLanguageToggle | Accessibility & Security | One-click toggle switching all application text between Kannada (ಕನ್ನಡ) and English |

## 3. Exhaustive Component Technical Specifications

### COMP-001: AppShell
**Category:** Layout & Navigation | **Identifier:** `COMP-001`

#### 1. Functional Purpose & Clinical Ergonomics
The `AppShell` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Master application container with responsive header, collapsible sidebar, and offline banner. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AppShellProps {
  id: 'COMP-001';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-002: ClinicHeader
**Category:** Layout & Navigation | **Identifier:** `COMP-002`

#### 1. Functional Purpose & Clinical Ergonomics
The `ClinicHeader` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Top navigation bar showing clinic name, ward code, active doctor name, sync badge, and language toggle. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicHeaderProps {
  id: 'COMP-002';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-003: RoleSidebar
**Category:** Layout & Navigation | **Identifier:** `COMP-003`

#### 1. Functional Purpose & Clinical Ergonomics
The `RoleSidebar` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Dynamic sidebar rendering only permitted navigation routes based on active user role. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RoleSidebarProps {
  id: 'COMP-003';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-004: BreadcrumbNav
**Category:** Layout & Navigation | **Identifier:** `COMP-004`

#### 1. Functional Purpose & Clinical Ergonomics
The `BreadcrumbNav` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Hierarchical navigation trail with deep-link support and keyboard tab focus. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BreadcrumbNavProps {
  id: 'COMP-004';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-005: TabBar
**Category:** Layout & Navigation | **Identifier:** `COMP-005`

#### 1. Functional Purpose & Clinical Ergonomics
The `TabBar` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Multi-tab sub-navigation for clinical encounters and patient longitudinal record sections. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TabBarProps {
  id: 'COMP-005';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-006: SplitPaneLayout
**Category:** Layout & Navigation | **Identifier:** `COMP-006`

#### 1. Functional Purpose & Clinical Ergonomics
The `SplitPaneLayout` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Dual-pane responsive layout for simultaneous patient record view and consultation notes entry. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SplitPaneLayoutProps {
  id: 'COMP-006';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-007: PageContainer
**Category:** Layout & Navigation | **Identifier:** `COMP-007`

#### 1. Functional Purpose & Clinical Ergonomics
The `PageContainer` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Standard content wrapper enforcing responsive margins, maximum width, and padding. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PageContainerProps {
  id: 'COMP-007';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-008: ActionToolbar
**Category:** Layout & Navigation | **Identifier:** `COMP-008`

#### 1. Functional Purpose & Clinical Ergonomics
The `ActionToolbar` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Sticky action bar with primary CTA, secondary actions, and cancel/back buttons. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ActionToolbarProps {
  id: 'COMP-008';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-009: MobileBottomNav
**Category:** Layout & Navigation | **Identifier:** `COMP-009`

#### 1. Functional Purpose & Clinical Ergonomics
The `MobileBottomNav` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Bottom icon bar optimized for tablet and handheld mobile screens. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MobileBottomNavProps {
  id: 'COMP-009';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-010: DrawerContainer
**Category:** Layout & Navigation | **Identifier:** `COMP-010`

#### 1. Functional Purpose & Clinical Ergonomics
The `DrawerContainer` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Slide-out side drawer for quick patient summary, sync queue, or notifications. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DrawerContainerProps {
  id: 'COMP-010';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-011: CollapsibleSection
**Category:** Layout & Navigation | **Identifier:** `COMP-011`

#### 1. Functional Purpose & Clinical Ergonomics
The `CollapsibleSection` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Accordion card with smooth expansion toggle and ARIA expanded state. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CollapsibleSectionProps {
  id: 'COMP-011';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-012: CardSurface
**Category:** Layout & Navigation | **Identifier:** `COMP-012`

#### 1. Functional Purpose & Clinical Ergonomics
The `CardSurface` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Elevated visual card container with standardized borders, radius, and shadows. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CardSurfaceProps {
  id: 'COMP-012';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-013: ModalContainer
**Category:** Layout & Navigation | **Identifier:** `COMP-013`

#### 1. Functional Purpose & Clinical Ergonomics
The `ModalContainer` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Accessible modal dialog overlay with focus trap, backdrop blur, and escape key listener. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ModalContainerProps {
  id: 'COMP-013';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-014: KeyboardShortcutGuide
**Category:** Layout & Navigation | **Identifier:** `COMP-014`

#### 1. Functional Purpose & Clinical Ergonomics
The `KeyboardShortcutGuide` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Floating cheat sheet displaying fast-action keyboard shortcuts for clinical workflows. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface KeyboardShortcutGuideProps {
  id: 'COMP-014';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-015: FooterStatusStrip
**Category:** Layout & Navigation | **Identifier:** `COMP-015`

#### 1. Functional Purpose & Clinical Ergonomics
The `FooterStatusStrip` component fulfills critical operational duties within the Layout & Navigation layer. Specifically, Bottom status strip displaying local SQLite sync state, memory usage, and software version. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FooterStatusStripProps {
  id: 'COMP-015';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-016: StatusBadge
**Category:** Data Display & Feedback | **Identifier:** `COMP-016`

#### 1. Functional Purpose & Clinical Ergonomics
The `StatusBadge` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Color-coded status chip for visit states, lab statuses, and triage urgency tiers. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StatusBadgeProps {
  id: 'COMP-016';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-017: ToastNotification
**Category:** Data Display & Feedback | **Identifier:** `COMP-017`

#### 1. Functional Purpose & Clinical Ergonomics
The `ToastNotification` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Auto-dismissing toast alert with success, warning, error, and info styles. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ToastNotificationProps {
  id: 'COMP-017';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-018: SystemAlertBanner
**Category:** Data Display & Feedback | **Identifier:** `COMP-018`

#### 1. Functional Purpose & Clinical Ergonomics
The `SystemAlertBanner` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Prominent full-width alert banner for network disconnection or emergency alerts. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SystemAlertBannerProps {
  id: 'COMP-018';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-019: EmptyStateDisplay
**Category:** Data Display & Feedback | **Identifier:** `COMP-019`

#### 1. Functional Purpose & Clinical Ergonomics
The `EmptyStateDisplay` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Illustrative placeholder with descriptive text and clear primary action button. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface EmptyStateDisplayProps {
  id: 'COMP-019';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-020: LoadingSkeletonCard
**Category:** Data Display & Feedback | **Identifier:** `COMP-020`

#### 1. Functional Purpose & Clinical Ergonomics
The `LoadingSkeletonCard` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Shimmering animated skeleton placeholder matching target content geometry. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LoadingSkeletonCardProps {
  id: 'COMP-020';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-021: LoadingSpinner
**Category:** Data Display & Feedback | **Identifier:** `COMP-021`

#### 1. Functional Purpose & Clinical Ergonomics
The `LoadingSpinner` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Lightweight SVG circular activity indicator with accessible aria-busy announce. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LoadingSpinnerProps {
  id: 'COMP-021';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-022: LinearProgressBar
**Category:** Data Display & Feedback | **Identifier:** `COMP-022`

#### 1. Functional Purpose & Clinical Ergonomics
The `LinearProgressBar` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Determinate and indeterminate progress bar for batch operations and sync progress. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LinearProgressBarProps {
  id: 'COMP-022';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-023: MetricStatCard
**Category:** Data Display & Feedback | **Identifier:** `COMP-023`

#### 1. Functional Purpose & Clinical Ergonomics
The `MetricStatCard` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, KPI stat card displaying numerical figure, trend sparkline, and percentage change. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MetricStatCardProps {
  id: 'COMP-023';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-024: DataTableGrid
**Category:** Data Display & Feedback | **Identifier:** `COMP-024`

#### 1. Functional Purpose & Clinical Ergonomics
The `DataTableGrid` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, High-performance virtualized table supporting sorting, filtering, and column resize. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DataTableGridProps {
  id: 'COMP-024';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-025: PaginationControl
**Category:** Data Display & Feedback | **Identifier:** `COMP-025`

#### 1. Functional Purpose & Clinical Ergonomics
The `PaginationControl` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Accessible pagination toolbar with page jump, size selector, and item counts. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PaginationControlProps {
  id: 'COMP-025';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-026: ConfirmationDialog
**Category:** Data Display & Feedback | **Identifier:** `COMP-026`

#### 1. Functional Purpose & Clinical Ergonomics
The `ConfirmationDialog` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Destructive action confirmation modal with explicit hazard warning and dual confirmation. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ConfirmationDialogProps {
  id: 'COMP-026';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-027: TooltipWrapper
**Category:** Data Display & Feedback | **Identifier:** `COMP-027`

#### 1. Functional Purpose & Clinical Ergonomics
The `TooltipWrapper` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Hover and focus triggered tooltip providing micro-help in Kannada and English. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TooltipWrapperProps {
  id: 'COMP-027';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-028: PopoverMenu
**Category:** Data Display & Feedback | **Identifier:** `COMP-028`

#### 1. Functional Purpose & Clinical Ergonomics
The `PopoverMenu` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Contextual action popover menu positioned dynamically next to trigger element. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PopoverMenuProps {
  id: 'COMP-028';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-029: TagCloud
**Category:** Data Display & Feedback | **Identifier:** `COMP-029`

#### 1. Functional Purpose & Clinical Ergonomics
The `TagCloud` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Interactive collection of chips for symptom tags, allergy labels, and diagnosis tags. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TagCloudProps {
  id: 'COMP-029';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-030: AuditDiffViewer
**Category:** Data Display & Feedback | **Identifier:** `COMP-030`

#### 1. Functional Purpose & Clinical Ergonomics
The `AuditDiffViewer` component fulfills critical operational duties within the Data Display & Feedback layer. Specifically, Side-by-side visual diff component showing before-and-after state changes in records. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AuditDiffViewerProps {
  id: 'COMP-030';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-031: TextInput
**Category:** Form Controls & Inputs | **Identifier:** `COMP-031`

#### 1. Functional Purpose & Clinical Ergonomics
The `TextInput` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Single-line text input with floating label, validation error icon, and clear button. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TextInputProps {
  id: 'COMP-031';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-032: MaskedPhoneInput
**Category:** Form Controls & Inputs | **Identifier:** `COMP-032`

#### 1. Functional Purpose & Clinical Ergonomics
The `MaskedPhoneInput` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Indian 10-digit mobile number input with +91 prefix and automatic formatting. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MaskedPhoneInputProps {
  id: 'COMP-032';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-033: AadhaarMaskedInput
**Category:** Form Controls & Inputs | **Identifier:** `COMP-033`

#### 1. Functional Purpose & Clinical Ergonomics
The `AadhaarMaskedInput` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, 12-digit national ID input with automated masking (XXXX-XXXX-1234) for privacy. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AadhaarMaskedInputProps {
  id: 'COMP-033';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-034: NumberInputStepper
**Category:** Form Controls & Inputs | **Identifier:** `COMP-034`

#### 1. Functional Purpose & Clinical Ergonomics
The `NumberInputStepper` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Numeric input with increment/decrement steppers and min/max clamping. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NumberInputStepperProps {
  id: 'COMP-034';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-035: SearchableCombobox
**Category:** Form Controls & Inputs | **Identifier:** `COMP-035`

#### 1. Functional Purpose & Clinical Ergonomics
The `SearchableCombobox` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Autocomplete dropdown with asynchronous search, keyboard navigation, and create-new option. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SearchableComboboxProps {
  id: 'COMP-035';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-036: SingleSelectDropdown
**Category:** Form Controls & Inputs | **Identifier:** `COMP-036`

#### 1. Functional Purpose & Clinical Ergonomics
The `SingleSelectDropdown` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Standard select menu with native mobile fallback and accessible keyboard navigation. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SingleSelectDropdownProps {
  id: 'COMP-036';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-037: MultiSelectCheckboxDropdown
**Category:** Form Controls & Inputs | **Identifier:** `COMP-037`

#### 1. Functional Purpose & Clinical Ergonomics
The `MultiSelectCheckboxDropdown` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Dropdown enabling multiple checkbox selections with selected count badges. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MultiSelectCheckboxDropdownProps {
  id: 'COMP-037';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-038: DatePickerCalendar
**Category:** Form Controls & Inputs | **Identifier:** `COMP-038`

#### 1. Functional Purpose & Clinical Ergonomics
The `DatePickerCalendar` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Accessible calendar popup supporting date selection with Kannada month labels. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DatePickerCalendarProps {
  id: 'COMP-038';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-039: TimePickerControl
**Category:** Form Controls & Inputs | **Identifier:** `COMP-039`

#### 1. Functional Purpose & Clinical Ergonomics
The `TimePickerControl` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, 12/24 hour time selector with AM/PM toggle and quick-select presets. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TimePickerControlProps {
  id: 'COMP-039';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-040: RadioGroupSelector
**Category:** Form Controls & Inputs | **Identifier:** `COMP-040`

#### 1. Functional Purpose & Clinical Ergonomics
The `RadioGroupSelector` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Accessible radio button group with arrow key navigation and label descriptions. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RadioGroupSelectorProps {
  id: 'COMP-040';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-041: CheckboxControl
**Category:** Form Controls & Inputs | **Identifier:** `COMP-041`

#### 1. Functional Purpose & Clinical Ergonomics
The `CheckboxControl` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Standard checkbox with custom checkmark icon, indeterminate state, and error styling. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CheckboxControlProps {
  id: 'COMP-041';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-042: ToggleSwitch
**Category:** Form Controls & Inputs | **Identifier:** `COMP-042`

#### 1. Functional Purpose & Clinical Ergonomics
The `ToggleSwitch` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Binary on/off toggle switch with smooth sliding animation and high-contrast focus ring. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ToggleSwitchProps {
  id: 'COMP-042';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-043: TextAreaInput
**Category:** Form Controls & Inputs | **Identifier:** `COMP-043`

#### 1. Functional Purpose & Clinical Ergonomics
The `TextAreaInput` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Multi-line text area with auto-expansion, character counter, and spellcheck toggle. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TextAreaInputProps {
  id: 'COMP-043';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-044: DigitalSignaturePad
**Category:** Form Controls & Inputs | **Identifier:** `COMP-044`

#### 1. Functional Purpose & Clinical Ergonomics
The `DigitalSignaturePad` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, HTML5 canvas signature pad for citizen consent and clinician sign-off with clear/undo. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DigitalSignaturePadProps {
  id: 'COMP-044';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-045: WebcamCaptureWidget
**Category:** Form Controls & Inputs | **Identifier:** `COMP-045`

#### 1. Functional Purpose & Clinical Ergonomics
The `WebcamCaptureWidget` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Browser webcam interface with face guide overlay, capture snapshot, and retake controls. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface WebcamCaptureWidgetProps {
  id: 'COMP-045';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-046: BarcodeScannerInput
**Category:** Form Controls & Inputs | **Identifier:** `COMP-046`

#### 1. Functional Purpose & Clinical Ergonomics
The `BarcodeScannerInput` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Hardware HID barcode scanner listener with debounce and audio beep feedback. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BarcodeScannerInputProps {
  id: 'COMP-046';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-047: FileUploadDropzone
**Category:** Form Controls & Inputs | **Identifier:** `COMP-047`

#### 1. Functional Purpose & Clinical Ergonomics
The `FileUploadDropzone` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Drag-and-drop document upload area with file size validation and thumbnail preview. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FileUploadDropzoneProps {
  id: 'COMP-047';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-048: PasswordInput
**Category:** Form Controls & Inputs | **Identifier:** `COMP-048`

#### 1. Functional Purpose & Clinical Ergonomics
The `PasswordInput` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Secure password field with visibility toggle, strength meter, and caps-lock warning. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PasswordInputProps {
  id: 'COMP-048';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-049: FormActionFooter
**Category:** Form Controls & Inputs | **Identifier:** `COMP-049`

#### 1. Functional Purpose & Clinical Ergonomics
The `FormActionFooter` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Standardized form button row with Submit, Reset, and Save Draft buttons. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FormActionFooterProps {
  id: 'COMP-049';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-050: FieldValidationError
**Category:** Form Controls & Inputs | **Identifier:** `COMP-050`

#### 1. Functional Purpose & Clinical Ergonomics
The `FieldValidationError` component fulfills critical operational duties within the Form Controls & Inputs layer. Specifically, Accessible inline error message with role='alert' and SVG warning icon. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FieldValidationErrorProps {
  id: 'COMP-050';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-051: PatientBanner
**Category:** Clinical & Consultation | **Identifier:** `COMP-051`

#### 1. Functional Purpose & Clinical Ergonomics
The `PatientBanner` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Persistent patient header displaying UHID, photo, name, age/gender, allergies, and vitals. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PatientBannerProps {
  id: 'COMP-051';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-052: VitalsGridDisplay
**Category:** Clinical & Consultation | **Identifier:** `COMP-052`

#### 1. Functional Purpose & Clinical Ergonomics
The `VitalsGridDisplay` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Structured grid displaying current visit vitals with abnormal value highlighting. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VitalsGridDisplayProps {
  id: 'COMP-052';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-053: VitalsTrendSparkline
**Category:** Clinical & Consultation | **Identifier:** `COMP-053`

#### 1. Functional Purpose & Clinical Ergonomics
The `VitalsTrendSparkline` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Miniature line chart showing systolic BP or blood sugar trend across past 5 visits. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VitalsTrendSparklineProps {
  id: 'COMP-053';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-054: DangerScoreBadge
**Category:** Clinical & Consultation | **Identifier:** `COMP-054`

#### 1. Functional Purpose & Clinical Ergonomics
The `DangerScoreBadge` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Early Warning Score (MEWS/PEWS) color-coded badge indicating clinical risk level. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DangerScoreBadgeProps {
  id: 'COMP-054';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-055: AllergyAlertChip
**Category:** Clinical & Consultation | **Identifier:** `COMP-055`

#### 1. Functional Purpose & Clinical Ergonomics
The `AllergyAlertChip` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, High-visibility red warning chip highlighting confirmed drug allergies on hover/click. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AllergyAlertChipProps {
  id: 'COMP-055';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-056: DiagnosisSearchCombobox
**Category:** Clinical & Consultation | **Identifier:** `COMP-056`

#### 1. Functional Purpose & Clinical Ergonomics
The `DiagnosisSearchCombobox` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Dual-search ICD-10 and SNOMED CT diagnosis selector with Kannada common terms. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DiagnosisSearchComboboxProps {
  id: 'COMP-056';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-057: ChiefComplaintSelector
**Category:** Clinical & Consultation | **Identifier:** `COMP-057`

#### 1. Functional Purpose & Clinical Ergonomics
The `ChiefComplaintSelector` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Interactive body map and common complaints grid for rapid symptom logging. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ChiefComplaintSelectorProps {
  id: 'COMP-057';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-058: ClinicalHistoryTimeline
**Category:** Clinical & Consultation | **Identifier:** `COMP-058`

#### 1. Functional Purpose & Clinical Ergonomics
The `ClinicalHistoryTimeline` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Vertical timeline depicting past diagnoses, prescriptions, and lab tests chronologically. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicalHistoryTimelineProps {
  id: 'COMP-058';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-059: ConsultationTimer
**Category:** Clinical & Consultation | **Identifier:** `COMP-059`

#### 1. Functional Purpose & Clinical Ergonomics
The `ConsultationTimer` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Discreet timer tracking duration of patient encounter for clinic workflow analytics. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ConsultationTimerProps {
  id: 'COMP-059';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-060: PediatricPercentileCard
**Category:** Clinical & Consultation | **Identifier:** `COMP-060`

#### 1. Functional Purpose & Clinical Ergonomics
The `PediatricPercentileCard` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, WHO child growth percentile card plotting weight-for-age and height-for-age. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PediatricPercentileCardProps {
  id: 'COMP-060';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-061: ANCEncounterCard
**Category:** Clinical & Consultation | **Identifier:** `COMP-061`

#### 1. Functional Purpose & Clinical Ergonomics
The `ANCEncounterCard` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Antenatal care tracker displaying trimester, expected delivery date, and high-risk flags. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ANCEncounterCardProps {
  id: 'COMP-061';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-062: NCDTrackingCard
**Category:** Clinical & Consultation | **Identifier:** `COMP-062`

#### 1. Functional Purpose & Clinical Ergonomics
The `NCDTrackingCard` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Chronic illness management summary displaying 3-month HbA1c and BP control metrics. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NCDTrackingCardProps {
  id: 'COMP-062';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-063: ClinicalNoteEditor
**Category:** Clinical & Consultation | **Identifier:** `COMP-063`

#### 1. Functional Purpose & Clinical Ergonomics
The `ClinicalNoteEditor` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Rich text SOAP clinical note editor with pre-filled physical examination templates. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicalNoteEditorProps {
  id: 'COMP-063';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-064: DrugAllergyModal
**Category:** Clinical & Consultation | **Identifier:** `COMP-064`

#### 1. Functional Purpose & Clinical Ergonomics
The `DrugAllergyModal` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Formal modal for recording new drug or food allergies with reaction severity. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DrugAllergyModalProps {
  id: 'COMP-064';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-065: BreakGlassAlertBanner
**Category:** Clinical & Consultation | **Identifier:** `COMP-065`

#### 1. Functional Purpose & Clinical Ergonomics
The `BreakGlassAlertBanner` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Prominent warning banner indicating encounter is running under emergency break-glass status. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BreakGlassAlertBannerProps {
  id: 'COMP-065';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-066: TeleconsultVideoFrame
**Category:** Clinical & Consultation | **Identifier:** `COMP-066`

#### 1. Functional Purpose & Clinical Ergonomics
The `TeleconsultVideoFrame` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, WebRTC video feed container with audio/video mute, end call, and network indicator. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TeleconsultVideoFrameProps {
  id: 'COMP-066';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-067: MedicalCertificateBuilder
**Category:** Clinical & Consultation | **Identifier:** `COMP-067`

#### 1. Functional Purpose & Clinical Ergonomics
The `MedicalCertificateBuilder` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Form generator for medical leave and fitness certificates with doctor digital seal. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MedicalCertificateBuilderProps {
  id: 'COMP-067';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-068: ClinicalSignoffModal
**Category:** Clinical & Consultation | **Identifier:** `COMP-068`

#### 1. Functional Purpose & Clinical Ergonomics
The `ClinicalSignoffModal` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Encounter completion dialog displaying final summary and PIN authorization prompt. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ClinicalSignoffModalProps {
  id: 'COMP-068';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-069: ReferralQuickTrigger
**Category:** Clinical & Consultation | **Identifier:** `COMP-069`

#### 1. Functional Purpose & Clinical Ergonomics
The `ReferralQuickTrigger` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Fast-action referral button linking consultation directly to 108 or hospital transfer. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReferralQuickTriggerProps {
  id: 'COMP-069';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-070: VoiceToTextButton
**Category:** Clinical & Consultation | **Identifier:** `COMP-070`

#### 1. Functional Purpose & Clinical Ergonomics
The `VoiceToTextButton` component fulfills critical operational duties within the Clinical & Consultation layer. Specifically, Microphone button activating client-side Web Speech API for Kannada clinical dictation. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VoiceToTextButtonProps {
  id: 'COMP-070';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-071: PrescriptionItemRow
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-071`

#### 1. Functional Purpose & Clinical Ergonomics
The `PrescriptionItemRow` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Single medication row: medicine name, dosage, frequency, food relation, and duration. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrescriptionItemRowProps {
  id: 'COMP-071';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-072: FrequencySelectorGroup
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-072`

#### 1. Functional Purpose & Clinical Ergonomics
The `FrequencySelectorGroup` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Button group for standard clinical frequencies (1-0-1, 1-1-1, 0-0-1, SOS, STAT). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FrequencySelectorGroupProps {
  id: 'COMP-072';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-073: FoodRelationToggle
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-073`

#### 1. Functional Purpose & Clinical Ergonomics
The `FoodRelationToggle` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Icon toggle for Before Food (ಊಟಕ್ಕೆ ಮುಂಚೆ) and After Food (ಊಟದ ನಂತರ). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FoodRelationToggleProps {
  id: 'COMP-073';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-074: DosageCalculator
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-074`

#### 1. Functional Purpose & Clinical Ergonomics
The `DosageCalculator` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Pediatric weight-based liquid dosage calculator (mg/kg/day to ml per dose). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DosageCalculatorProps {
  id: 'COMP-074';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-075: DrugInteractionAlertCard
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-075`

#### 1. Functional Purpose & Clinical Ergonomics
The `DrugInteractionAlertCard` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Card detailing clinical severity of detected drug-drug interaction with override reasons. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DrugInteractionAlertCardProps {
  id: 'COMP-075';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-076: StockAvailabilityPill
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-076`

#### 1. Functional Purpose & Clinical Ergonomics
The `StockAvailabilityPill` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Color badge indicating dispensary stock: In-Stock (Green), Low (Orange), Stockout (Red). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockAvailabilityPillProps {
  id: 'COMP-076';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-077: BatchNumberBadge
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-077`

#### 1. Functional Purpose & Clinical Ergonomics
The `BatchNumberBadge` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Label showing assigned medicine batch number and expiry date based on FEFO logic. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BatchNumberBadgeProps {
  id: 'COMP-077';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-078: DispensingQuantityStepper
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-078`

#### 1. Functional Purpose & Clinical Ergonomics
The `DispensingQuantityStepper` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Validated counter ensuring dispensed quantity does not exceed prescribed or batch quantity. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DispensingQuantityStepperProps {
  id: 'COMP-078';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-079: BarcodeScanMatcher
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-079`

#### 1. Functional Purpose & Clinical Ergonomics
The `BarcodeScanMatcher` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Interactive scanner matching physical barcode against electronic prescription line item. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BarcodeScanMatcherProps {
  id: 'COMP-079';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-080: MedicationCounselingChecklist
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-080`

#### 1. Functional Purpose & Clinical Ergonomics
The `MedicationCounselingChecklist` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Interactive checklist verifying patient received verbal instructions on dosage and side effects. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MedicationCounselingChecklistProps {
  id: 'COMP-080';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-081: PrescriptionPrintLayout
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-081`

#### 1. Functional Purpose & Clinical Ergonomics
The `PrescriptionPrintLayout` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Print-optimized DOM structure formatting prescription for A4 or thermal printer. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrescriptionPrintLayoutProps {
  id: 'COMP-081';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-082: SubstituteDrugModal
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-082`

#### 1. Functional Purpose & Clinical Ergonomics
The `SubstituteDrugModal` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Pharmacist substitution dialog suggesting bio-equivalent in-stock generic molecules. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SubstituteDrugModalProps {
  id: 'COMP-082';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-083: PartialDispenseBanner
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-083`

#### 1. Functional Purpose & Clinical Ergonomics
The `PartialDispenseBanner` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Warning notice detailing remaining un-dispensed medication balance. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PartialDispenseBannerProps {
  id: 'COMP-083';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-084: RefillApprovalCard
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-084`

#### 1. Functional Purpose & Clinical Ergonomics
The `RefillApprovalCard` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Chronic NCD 30-day medication refill review card with remaining allowed refills. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RefillApprovalCardProps {
  id: 'COMP-084';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-085: ControlledDrugVerification
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-085`

#### 1. Functional Purpose & Clinical Ergonomics
The `ControlledDrugVerification` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Dual-signature prompt requiring pharmacist and doctor authentication before dispense. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ControlledDrugVerificationProps {
  id: 'COMP-085';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-086: FormularySearchInput
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-086`

#### 1. Functional Purpose & Clinical Ergonomics
The `FormularySearchInput` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Fast filter input searching through clinic 52-essential-drug list. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface FormularySearchInputProps {
  id: 'COMP-086';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-087: PrescriptionHistoryTable
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-087`

#### 1. Functional Purpose & Clinical Ergonomics
The `PrescriptionHistoryTable` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Table listing past prescriptions with quick 'Re-order Same Regimen' action. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrescriptionHistoryTableProps {
  id: 'COMP-087';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-088: MedicationLabelPreview
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-088`

#### 1. Functional Purpose & Clinical Ergonomics
The `MedicationLabelPreview` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Preview widget showing bilingual patient instructions as they will appear on strip sticker. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MedicationLabelPreviewProps {
  id: 'COMP-088';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-089: StockExpiryWarningCard
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-089`

#### 1. Functional Purpose & Clinical Ergonomics
The `StockExpiryWarningCard` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Alert card highlighting batches approaching expiration within 30/60/90 days. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockExpiryWarningCardProps {
  id: 'COMP-089';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-090: PharmacyReconciliationRow
**Category:** Prescription & Pharmacy | **Identifier:** `COMP-090`

#### 1. Functional Purpose & Clinical Ergonomics
The `PharmacyReconciliationRow` component fulfills critical operational duties within the Prescription & Pharmacy layer. Specifically, Row comparing system calculated stock against physical count with variance display. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PharmacyReconciliationRowProps {
  id: 'COMP-090';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-091: OPDTokenTicket
**Category:** Queue & Triage | **Identifier:** `COMP-091`

#### 1. Functional Purpose & Clinical Ergonomics
The `OPDTokenTicket` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Thermal ticket layout displaying token number, date, department, and barcode. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface OPDTokenTicketProps {
  id: 'COMP-091';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-092: QueuePositionCard
**Category:** Queue & Triage | **Identifier:** `COMP-092`

#### 1. Functional Purpose & Clinical Ergonomics
The `QueuePositionCard` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Widget indicating current position in line and estimated wait time in minutes. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QueuePositionCardProps {
  id: 'COMP-092';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-093: PublicQueueBoard
**Category:** Queue & Triage | **Identifier:** `COMP-093`

#### 1. Functional Purpose & Clinical Ergonomics
The `PublicQueueBoard` component fulfills critical operational duties within the Queue & Triage layer. Specifically, High-contrast public TV display board showing active token numbers by doctor cabin. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PublicQueueBoardProps {
  id: 'COMP-093';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-094: AudioAnnouncementTrigger
**Category:** Queue & Triage | **Identifier:** `COMP-094`

#### 1. Functional Purpose & Clinical Ergonomics
The `AudioAnnouncementTrigger` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Audio speech synthesizer calling patient token in Kannada and English. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AudioAnnouncementTriggerProps {
  id: 'COMP-094';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-095: PatientCallButton
**Category:** Queue & Triage | **Identifier:** `COMP-095`

#### 1. Functional Purpose & Clinical Ergonomics
The `PatientCallButton` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Doctor console button to advance queue, call next patient, or mark as no-show. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PatientCallButtonProps {
  id: 'COMP-095';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-096: PriorityQueueBadge
**Category:** Queue & Triage | **Identifier:** `COMP-096`

#### 1. Functional Purpose & Clinical Ergonomics
The `PriorityQueueBadge` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Badge designating Emergency (Red), Senior (Orange), Antenatal (Purple), or Normal (Blue). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PriorityQueueBadgeProps {
  id: 'COMP-096';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-097: TriageVitalsCard
**Category:** Queue & Triage | **Identifier:** `COMP-097`

#### 1. Functional Purpose & Clinical Ergonomics
The `TriageVitalsCard` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Compact card summarizing intake vitals for quick doctor review before exam. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TriageVitalsCardProps {
  id: 'COMP-097';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-098: BloodPressureDial
**Category:** Queue & Triage | **Identifier:** `COMP-098`

#### 1. Functional Purpose & Clinical Ergonomics
The `BloodPressureDial` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Gauge visualization indicating normal, pre-hypertension, or Stage 1/2 hypertension. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BloodPressureDialProps {
  id: 'COMP-098';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-099: OxygenSaturationIndicator
**Category:** Queue & Triage | **Identifier:** `COMP-099`

#### 1. Functional Purpose & Clinical Ergonomics
The `OxygenSaturationIndicator` component fulfills critical operational duties within the Queue & Triage layer. Specifically, SpO2 gauge with immediate hypoxia alarm trigger below 94%. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface OxygenSaturationIndicatorProps {
  id: 'COMP-099';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-100: BloodGlucoseBadge
**Category:** Queue & Triage | **Identifier:** `COMP-100`

#### 1. Functional Purpose & Clinical Ergonomics
The `BloodGlucoseBadge` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Color-coded glucose reading badge (Normal, Impaired, Severe Hyperglycemia). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BloodGlucoseBadgeProps {
  id: 'COMP-100';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-101: QueueReassignmentModal
**Category:** Queue & Triage | **Identifier:** `COMP-101`

#### 1. Functional Purpose & Clinical Ergonomics
The `QueueReassignmentModal` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Supervisor dialog to transfer patient between doctor cabins during unexpected delay. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QueueReassignmentModalProps {
  id: 'COMP-101';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-102: ExpressQueueFilter
**Category:** Queue & Triage | **Identifier:** `COMP-102`

#### 1. Functional Purpose & Clinical Ergonomics
The `ExpressQueueFilter` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Filter tab isolating priority demographics for fast triage intake. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ExpressQueueFilterProps {
  id: 'COMP-102';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-103: NoShowResolutionModal
**Category:** Queue & Triage | **Identifier:** `COMP-103`

#### 1. Functional Purpose & Clinical Ergonomics
The `NoShowResolutionModal` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Handling absent patients: recall, delay 3 positions, or cancel token. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NoShowResolutionModalProps {
  id: 'COMP-103';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-104: TriageQueueTable
**Category:** Queue & Triage | **Identifier:** `COMP-104`

#### 1. Functional Purpose & Clinical Ergonomics
The `TriageQueueTable` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Staff nurse table displaying awaiting triage patients with elapsed waiting time. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TriageQueueTableProps {
  id: 'COMP-104';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-105: QueueThroughputGauge
**Category:** Queue & Triage | **Identifier:** `COMP-105`

#### 1. Functional Purpose & Clinical Ergonomics
The `QueueThroughputGauge` component fulfills critical operational duties within the Queue & Triage layer. Specifically, Speedometer gauge showing hourly citizen intake rate vs target throughput. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QueueThroughputGaugeProps {
  id: 'COMP-105';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-106: LabOrderRequisitionCard
**Category:** Diagnostics & Lab | **Identifier:** `COMP-106`

#### 1. Functional Purpose & Clinical Ergonomics
The `LabOrderRequisitionCard` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Doctor order card specifying required diagnostic tests, clinical indication, and fasting state. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabOrderRequisitionCardProps {
  id: 'COMP-106';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-107: SpecimenCollectionRow
**Category:** Diagnostics & Lab | **Identifier:** `COMP-107`

#### 1. Functional Purpose & Clinical Ergonomics
The `SpecimenCollectionRow` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Row recording phlebotomy blood draw or urine sample receipt with vial barcode. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SpecimenCollectionRowProps {
  id: 'COMP-107';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-108: VialBarcodeLabel
**Category:** Diagnostics & Lab | **Identifier:** `COMP-108`

#### 1. Functional Purpose & Clinical Ergonomics
The `VialBarcodeLabel` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, 25mm x 50mm thermal barcode label for blood collection tubes. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VialBarcodeLabelProps {
  id: 'COMP-108';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-109: RapidTestResultInput
**Category:** Diagnostics & Lab | **Identifier:** `COMP-109`

#### 1. Functional Purpose & Clinical Ergonomics
The `RapidTestResultInput` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Radio selector for qualitative rapid POC tests (Positive, Negative, Inconclusive). It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface RapidTestResultInputProps {
  id: 'COMP-109';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-110: HematologyResultGrid
**Category:** Diagnostics & Lab | **Identifier:** `COMP-110`

#### 1. Functional Purpose & Clinical Ergonomics
The `HematologyResultGrid` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Grid for complete blood count parameters with low/normal/high reference flags. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface HematologyResultGridProps {
  id: 'COMP-110';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-111: CriticalLabPanicBanner
**Category:** Diagnostics & Lab | **Identifier:** `COMP-111`

#### 1. Functional Purpose & Clinical Ergonomics
The `CriticalLabPanicBanner` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Flashing alert banner displayed when lab result falls into critical panic range. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface CriticalLabPanicBannerProps {
  id: 'COMP-111';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-112: LabReportPrintLayout
**Category:** Diagnostics & Lab | **Identifier:** `COMP-112`

#### 1. Functional Purpose & Clinical Ergonomics
The `LabReportPrintLayout` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Bilingual A4 diagnostic report format with technician and doctor sign-off. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabReportPrintLayoutProps {
  id: 'COMP-112';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-113: AnalyzerConnectionStatus
**Category:** Diagnostics & Lab | **Identifier:** `COMP-113`

#### 1. Functional Purpose & Clinical Ergonomics
The `AnalyzerConnectionStatus` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Badge indicating USB/Serial connectivity status to automated hematology analyzer. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface AnalyzerConnectionStatusProps {
  id: 'COMP-113';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-114: SpecimenRejectionModal
**Category:** Diagnostics & Lab | **Identifier:** `COMP-114`

#### 1. Functional Purpose & Clinical Ergonomics
The `SpecimenRejectionModal` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Logging hemolyzed or clotted samples with mandatory request for re-draw. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SpecimenRejectionModalProps {
  id: 'COMP-114';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-115: ReagentLotExpiryBadge
**Category:** Diagnostics & Lab | **Identifier:** `COMP-115`

#### 1. Functional Purpose & Clinical Ergonomics
The `ReagentLotExpiryBadge` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Tracking test kit lot numbers, open-vial expiration, and quality control status. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReagentLotExpiryBadgeProps {
  id: 'COMP-115';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-116: ExternalLabReferralCard
**Category:** Diagnostics & Lab | **Identifier:** `COMP-116`

#### 1. Functional Purpose & Clinical Ergonomics
The `ExternalLabReferralCard` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Packing manifest for samples transported to central municipal referral lab. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ExternalLabReferralCardProps {
  id: 'COMP-116';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-117: LabWorksheetView
**Category:** Diagnostics & Lab | **Identifier:** `COMP-117`

#### 1. Functional Purpose & Clinical Ergonomics
The `LabWorksheetView` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Batch worksheet enabling technician to record results for multiple patients concurrently. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabWorksheetViewProps {
  id: 'COMP-117';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-118: UrineAnalysisGrid
**Category:** Diagnostics & Lab | **Identifier:** `COMP-118`

#### 1. Functional Purpose & Clinical Ergonomics
The `UrineAnalysisGrid` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Dipstick grid for protein, glucose, ketones, urobilinogen, and leukocyte esterase. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface UrineAnalysisGridProps {
  id: 'COMP-118';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-119: MicroscopyResultForm
**Category:** Diagnostics & Lab | **Identifier:** `COMP-119`

#### 1. Functional Purpose & Clinical Ergonomics
The `MicroscopyResultForm` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Free-text and structured findings form for stool, urine, and sputum smear exams. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface MicroscopyResultFormProps {
  id: 'COMP-119';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-120: LabTurnaroundTimeBadge
**Category:** Diagnostics & Lab | **Identifier:** `COMP-120`

#### 1. Functional Purpose & Clinical Ergonomics
The `LabTurnaroundTimeBadge` component fulfills critical operational duties within the Diagnostics & Lab layer. Specifically, Timer badge showing elapsed time from sample collection to authorized result. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LabTurnaroundTimeBadgeProps {
  id: 'COMP-120';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-121: StockLevelIndicator
**Category:** Inventory & Logistics | **Identifier:** `COMP-121`

#### 1. Functional Purpose & Clinical Ergonomics
The `StockLevelIndicator` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Bar indicator displaying current stock percentage against minimum reorder point. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockLevelIndicatorProps {
  id: 'COMP-121';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-122: ReorderPointAlert
**Category:** Inventory & Logistics | **Identifier:** `COMP-122`

#### 1. Functional Purpose & Clinical Ergonomics
The `ReorderPointAlert` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Warning card indicating item has fallen below 7-day safety buffer threshold. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReorderPointAlertProps {
  id: 'COMP-122';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-123: TemperatureLogGraph
**Category:** Inventory & Logistics | **Identifier:** `COMP-123`

#### 1. Functional Purpose & Clinical Ergonomics
The `TemperatureLogGraph` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Interactive line chart plotting refrigerator telemetry with upper/lower excursion lines. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface TemperatureLogGraphProps {
  id: 'COMP-123';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-124: ColdChainBreachModal
**Category:** Inventory & Logistics | **Identifier:** `COMP-124`

#### 1. Functional Purpose & Clinical Ergonomics
The `ColdChainBreachModal` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Urgent alert form recording temperature breach duration and vaccine viability check. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ColdChainBreachModalProps {
  id: 'COMP-124';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-125: GoodsReceiptVerification
**Category:** Inventory & Logistics | **Identifier:** `COMP-125`

#### 1. Functional Purpose & Clinical Ergonomics
The `GoodsReceiptVerification` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Checklist matching delivery invoice against physical boxes from central depot. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface GoodsReceiptVerificationProps {
  id: 'COMP-125';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-126: StockTransferCard
**Category:** Inventory & Logistics | **Identifier:** `COMP-126`

#### 1. Functional Purpose & Clinical Ergonomics
The `StockTransferCard` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Inter-clinic transfer manifest detailing batch, quantity, and destination clinic. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface StockTransferCardProps {
  id: 'COMP-126';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-127: QuarantineActionDialog
**Category:** Inventory & Logistics | **Identifier:** `COMP-127`

#### 1. Functional Purpose & Clinical Ergonomics
The `QuarantineActionDialog` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Securing expired, damaged, or recalled stock with photographic evidence upload. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface QuarantineActionDialogProps {
  id: 'COMP-127';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-128: PhysicalStocktakeRow
**Category:** Inventory & Logistics | **Identifier:** `COMP-128`

#### 1. Functional Purpose & Clinical Ergonomics
The `PhysicalStocktakeRow` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Audit worksheet row for recording physical shelf count vs software ledger. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PhysicalStocktakeRowProps {
  id: 'COMP-128';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-129: VaccineVialMonitorChip
**Category:** Inventory & Logistics | **Identifier:** `COMP-129`

#### 1. Functional Purpose & Clinical Ergonomics
The `VaccineVialMonitorChip` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, VVM Stage 1 to 4 selector determining whether vaccine can be administered. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface VaccineVialMonitorChipProps {
  id: 'COMP-129';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-130: DailyConsumptionCard
**Category:** Inventory & Logistics | **Identifier:** `COMP-130`

#### 1. Functional Purpose & Clinical Ergonomics
The `DailyConsumptionCard` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Summary of items deducted through dispensing during active clinic day. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DailyConsumptionCardProps {
  id: 'COMP-130';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-131: DepotIndentBuilder
**Category:** Inventory & Logistics | **Identifier:** `COMP-131`

#### 1. Functional Purpose & Clinical Ergonomics
The `DepotIndentBuilder` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Automated monthly indent generator calculating suggested order based on consumption. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DepotIndentBuilderProps {
  id: 'COMP-131';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-132: BatchTraceabilityViewer
**Category:** Inventory & Logistics | **Identifier:** `COMP-132`

#### 1. Functional Purpose & Clinical Ergonomics
The `BatchTraceabilityViewer` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Audit trail showing complete lifecycle of a batch from receipt to citizen dispensation. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BatchTraceabilityViewerProps {
  id: 'COMP-132';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-133: BiomedicalWasteLogForm
**Category:** Inventory & Logistics | **Identifier:** `COMP-133`

#### 1. Functional Purpose & Clinical Ergonomics
The `BiomedicalWasteLogForm` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Color-coded waste bin weighing entry (Yellow, Red, Blue, White) before vendor pickup. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BiomedicalWasteLogFormProps {
  id: 'COMP-133';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-134: EmergencyStockEmergencyButton
**Category:** Inventory & Logistics | **Identifier:** `COMP-134`

#### 1. Functional Purpose & Clinical Ergonomics
The `EmergencyStockEmergencyButton` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Fast SOS button alerting Zonal Pharmacist to impending stockout of lifesaving drugs. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface EmergencyStockEmergencyButtonProps {
  id: 'COMP-134';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-135: InventoryValuationWidget
**Category:** Inventory & Logistics | **Identifier:** `COMP-135`

#### 1. Functional Purpose & Clinical Ergonomics
The `InventoryValuationWidget` component fulfills critical operational duties within the Inventory & Logistics layer. Specifically, Financial summary of total medicines held on premises at government procurement rates. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface InventoryValuationWidgetProps {
  id: 'COMP-135';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-136: NetworkConnectivityBanner
**Category:** Offline & Synchronization | **Identifier:** `COMP-136`

#### 1. Functional Purpose & Clinical Ergonomics
The `NetworkConnectivityBanner` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Floating banner alerting user of Online, Degraded (2G/3G), or Offline network state. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface NetworkConnectivityBannerProps {
  id: 'COMP-136';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-137: SyncQueueDrawer
**Category:** Offline & Synchronization | **Identifier:** `COMP-137`

#### 1. Functional Purpose & Clinical Ergonomics
The `SyncQueueDrawer` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Slide-over drawer displaying pending local mutations waiting for network reconnection. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SyncQueueDrawerProps {
  id: 'COMP-137';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-138: ConflictDiffModal
**Category:** Offline & Synchronization | **Identifier:** `COMP-138`

#### 1. Functional Purpose & Clinical Ergonomics
The `ConflictDiffModal` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Side-by-side comparison modal allowing clinician to resolve conflicting edits. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ConflictDiffModalProps {
  id: 'COMP-138';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-139: LocalDiskQuotaMeter
**Category:** Offline & Synchronization | **Identifier:** `COMP-139`

#### 1. Functional Purpose & Clinical Ergonomics
The `LocalDiskQuotaMeter` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Storage meter displaying IndexedDB and SQLite disk consumption on clinic device. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface LocalDiskQuotaMeterProps {
  id: 'COMP-139';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-140: OfflineLoginIndicator
**Category:** Offline & Synchronization | **Identifier:** `COMP-140`

#### 1. Functional Purpose & Clinical Ergonomics
The `OfflineLoginIndicator` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Badge showing user is authenticated via local SQLite cached credentials. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface OfflineLoginIndicatorProps {
  id: 'COMP-140';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-141: ManualSyncTriggerButton
**Category:** Offline & Synchronization | **Identifier:** `COMP-141`

#### 1. Functional Purpose & Clinical Ergonomics
The `ManualSyncTriggerButton` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Button triggering immediate cryptographic synchronization handshake with central cloud. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ManualSyncTriggerButtonProps {
  id: 'COMP-141';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-142: PeerSyncDiscoveryBadge
**Category:** Offline & Synchronization | **Identifier:** `COMP-142`

#### 1. Functional Purpose & Clinical Ergonomics
The `PeerSyncDiscoveryBadge` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Indicator showing tablet is connected to local clinic mini-PC via LAN / mDNS. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PeerSyncDiscoveryBadgeProps {
  id: 'COMP-142';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-143: SyncErrorAlertCard
**Category:** Offline & Synchronization | **Identifier:** `COMP-143`

#### 1. Functional Purpose & Clinical Ergonomics
The `SyncErrorAlertCard` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Notification card explaining rejected sync mutation with automated recovery instructions. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SyncErrorAlertCardProps {
  id: 'COMP-143';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-144: UnsavedChangesGuardModal
**Category:** Offline & Synchronization | **Identifier:** `COMP-144`

#### 1. Functional Purpose & Clinical Ergonomics
The `UnsavedChangesGuardModal` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Navigation blocker preventing accidental exit from form before local persistence. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface UnsavedChangesGuardModalProps {
  id: 'COMP-144';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-145: DatabaseCompactButton
**Category:** Offline & Synchronization | **Identifier:** `COMP-145`

#### 1. Functional Purpose & Clinical Ergonomics
The `DatabaseCompactButton` component fulfills critical operational duties within the Offline & Synchronization layer. Specifically, Administrative maintenance button triggering local SQLite VACUUM and index rebuild. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface DatabaseCompactButtonProps {
  id: 'COMP-145';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-146: PrintPreviewModal
**Category:** Printing & Export | **Identifier:** `COMP-146`

#### 1. Functional Purpose & Clinical Ergonomics
The `PrintPreviewModal` component fulfills critical operational duties within the Printing & Export layer. Specifically, Modal rendering exact print page layout before sending to local hardware printer. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrintPreviewModalProps {
  id: 'COMP-146';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-147: ThermalPrinterSelector
**Category:** Printing & Export | **Identifier:** `COMP-147`

#### 1. Functional Purpose & Clinical Ergonomics
The `ThermalPrinterSelector` component fulfills critical operational duties within the Printing & Export layer. Specifically, Settings dropdown selecting network or USB ESC/POS 80mm thermal receipt printer. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ThermalPrinterSelectorProps {
  id: 'COMP-147';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-148: PDFExportProgressModal
**Category:** Printing & Export | **Identifier:** `COMP-148`

#### 1. Functional Purpose & Clinical Ergonomics
The `PDFExportProgressModal` component fulfills critical operational duties within the Printing & Export layer. Specifically, Progress dialog generating client-side encrypted PDF for citizen records. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PDFExportProgressModalProps {
  id: 'COMP-148';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-149: KannadaPrintFontInjector
**Category:** Printing & Export | **Identifier:** `COMP-149`

#### 1. Functional Purpose & Clinical Ergonomics
The `KannadaPrintFontInjector` component fulfills critical operational duties within the Printing & Export layer. Specifically, CSS print engine injecting embedded Kannada Noto Serif fonts for clean thermal print. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface KannadaPrintFontInjectorProps {
  id: 'COMP-149';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-150: BarcodePrintGenerator
**Category:** Printing & Export | **Identifier:** `COMP-150`

#### 1. Functional Purpose & Clinical Ergonomics
The `BarcodePrintGenerator` component fulfills critical operational duties within the Printing & Export layer. Specifically, Client-side SVG Code-128 barcode generator for patient wristbands and vials. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BarcodePrintGeneratorProps {
  id: 'COMP-150';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-151: ReprintAuthorizationModal
**Category:** Printing & Export | **Identifier:** `COMP-151`

#### 1. Functional Purpose & Clinical Ergonomics
The `ReprintAuthorizationModal` component fulfills critical operational duties within the Printing & Export layer. Specifically, Supervisor PIN prompt required before reprinting prescription or OPD token. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ReprintAuthorizationModalProps {
  id: 'COMP-151';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-152: PrintAuditNotifier
**Category:** Printing & Export | **Identifier:** `COMP-152`

#### 1. Functional Purpose & Clinical Ergonomics
The `PrintAuditNotifier` component fulfills critical operational duties within the Printing & Export layer. Specifically, Silent background hook recording print event and document hash into WORM audit ledger. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrintAuditNotifierProps {
  id: 'COMP-152';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-153: SkipToContentLink
**Category:** Accessibility & Security | **Identifier:** `COMP-153`

#### 1. Functional Purpose & Clinical Ergonomics
The `SkipToContentLink` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Hidden accessible anchor allowing keyboard users to bypass header navigation. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SkipToContentLinkProps {
  id: 'COMP-153';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-154: ScreenReaderLiveRegion
**Category:** Accessibility & Security | **Identifier:** `COMP-154`

#### 1. Functional Purpose & Clinical Ergonomics
The `ScreenReaderLiveRegion` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Aria-live polite and assertive announcer for dynamic state updates. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface ScreenReaderLiveRegionProps {
  id: 'COMP-154';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-155: SessionInactivityWarningModal
**Category:** Accessibility & Security | **Identifier:** `COMP-155`

#### 1. Functional Purpose & Clinical Ergonomics
The `SessionInactivityWarningModal` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Countdown modal warning clinician of session logout due to 15 minutes of inactivity. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface SessionInactivityWarningModalProps {
  id: 'COMP-155';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-156: BreakGlassConfirmDialog
**Category:** Accessibility & Security | **Identifier:** `COMP-156`

#### 1. Functional Purpose & Clinical Ergonomics
The `BreakGlassConfirmDialog` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Dual-confirmation dialog capturing clinical justification for emergency access. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface BreakGlassConfirmDialogProps {
  id: 'COMP-156';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-157: PinPadInput
**Category:** Accessibility & Security | **Identifier:** `COMP-157`

#### 1. Functional Purpose & Clinical Ergonomics
The `PinPadInput` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Touchscreen on-screen numeric keypad for quick 4-digit PIN authentication. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PinPadInputProps {
  id: 'COMP-157';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-158: PrivacyMaskToggle
**Category:** Accessibility & Security | **Identifier:** `COMP-158`

#### 1. Functional Purpose & Clinical Ergonomics
The `PrivacyMaskToggle` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Eye icon button allowing clinician to blur sensitive HIV/mental health notes on screen. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface PrivacyMaskToggleProps {
  id: 'COMP-158';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-159: HighContrastModeToggle
**Category:** Accessibility & Security | **Identifier:** `COMP-159`

#### 1. Functional Purpose & Clinical Ergonomics
The `HighContrastModeToggle` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, Header button switching UI to 7:1 contrast ratio for low-vision clinic operators. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface HighContrastModeToggleProps {
  id: 'COMP-159';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---

### COMP-160: KannadaLanguageToggle
**Category:** Accessibility & Security | **Identifier:** `COMP-160`

#### 1. Functional Purpose & Clinical Ergonomics
The `KannadaLanguageToggle` component fulfills critical operational duties within the Accessibility & Security layer. Specifically, One-click toggle switching all application text between Kannada (ಕನ್ನಡ) and English. It provides deterministic behavior across desktop, tablet, and touch-screen clinic terminals.

#### 2. Input Properties & Output Events Contract
- **Core Props:** `id`, `className`, `variant`, `size`, `isDisabled`, `isLoading`, `locale` (`kn-IN` | `en-IN`).
- **Event Dispatches:** `onChange`, `onAction`, `onFocus`, `onError`, `onRetry`.
- **Validation Contract:** Enforces strict boundary checks; invalid input sets `aria-invalid='true'` and displays localized error message.

#### 3. Visual States & Transitions
- **Default:** Clean neutral surface styling with crisp border contrast conforming to BBMP Healthcare Design Tokens.
- **Loading / Skeleton:** Displays smooth shimmer animation while data resolves asynchronously.
- **Disabled:** Rendered with 45% opacity, `cursor: not-allowed`, and pointer events blocked.
- **Error / Warning:** Outer ring highlights in Crimson Red (`#DE350B`) or Alert Amber (`#FFAB00`) with assistive icon.
- **Offline Mode:** Displays localized offline badge when underlying mutations are cached locally.

#### 4. Accessibility (WCAG 2.1 AA) & Bilingual Support
- **Keyboard Interactivity:** Standard tab order (`tabindex='0'`); navigable via arrow keys, Space, and Enter.
- **ARIA Attributes:** Full support for `role`, `aria-label`, `aria-describedby`, and `aria-live` where appropriate.
- **Kannada Localization:** Dynamic font rendering using `Noto Sans Kannada` with line-height buffer preventing ligature truncation.

#### 5. Documentation-Only TypeScript Specification
```typescript
// DOCUMENTATION-ONLY TYPESCRIPT
export interface KannadaLanguageToggleProps {
  id: 'COMP-160';
  ariaLabel?: string;
  locale?: 'kn-IN' | 'en-IN';
  isOffline?: boolean;
  onStateChange?: (state: unknown) => void;
}
```

---
