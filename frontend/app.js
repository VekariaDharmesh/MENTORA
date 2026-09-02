/**
 * MENTORE — Full Product Suite & Pedagogical Engine
 * Complete end-to-end flow with Checkpoint, Adaptive Misconception, and Teacher Brain
 */

(function () {
  function initSuite() {
    try {
      // ----------------------------------------------------------------------
      // 1. SCREEN VIEW ROUTER (14 Views)
      // ----------------------------------------------------------------------
      const views = {
        'landing': document.getElementById('view-landing'),
        'onboarding': document.getElementById('view-onboarding'),
        'dashboard': document.getElementById('view-dashboard'),
        'create-lesson': document.getElementById('view-create-lesson'),
        'prep': document.getElementById('view-prep'),
        'player': document.getElementById('view-player'),
        'assessment': document.getElementById('view-assessment'),
        'report': document.getElementById('view-report'),
        'learning-path': document.getElementById('view-learning-path'),
        'library': document.getElementById('view-library'),
        'progress': document.getElementById('view-progress'),
        'settings': document.getElementById('view-settings'),
        'fallback': document.getElementById('view-fallback'),
        'empty': document.getElementById('view-empty')
      };

      // Production Header Elements
      const siteHeader = document.getElementById('site-nav-header');
      const navLinks = document.querySelectorAll('.nav-item-link');
      const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
      const mobileNavPanel = document.getElementById('mobile-nav-panel');

      // Scroll event for production header
      window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
          siteHeader?.classList.add('is-scrolled');
        } else {
          siteHeader?.classList.remove('is-scrolled');
        }
      }, { passive: true });

      // Mobile Menu Toggle
      mobileMenuToggle?.addEventListener('click', () => {
        const isOpen = mobileNavPanel?.classList.toggle('is-open');
        mobileMenuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });

      function switchScreen(screenKey) {
        if (!views[screenKey]) screenKey = 'landing';

        // Hide all views
        Object.keys(views).forEach(k => {
          if (views[k]) views[k].classList.remove('is-visible');
        });

        // Show target view
        views[screenKey].classList.add('is-visible');
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Close mobile menu if open
        if (mobileNavPanel?.classList.contains('is-open')) {
          mobileNavPanel.classList.remove('is-open');
          mobileMenuToggle?.setAttribute('aria-expanded', 'false');
        }

        // Update Header Navigation Active Indicator (understated 2px bottom line)
        navLinks.forEach(link => {
          const target = link.getAttribute('data-screen-target');
          if (target === screenKey) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });

        // Specific screen hooks
        if (screenKey === 'prep') {
          runPrepSimulation();
        } else if (screenKey === 'player') {
          startPlayerSimulation();
        }
      }

      // Generic [data-screen-target] clicks
      document.querySelectorAll('[data-screen-target]').forEach(elem => {
        elem.addEventListener('click', (e) => {
          e.preventDefault();
          const target = elem.getAttribute('data-screen-target');
          window.location.hash = target;
          switchScreen(target);
        });
      });

      // Hash change listener
      window.addEventListener('hashchange', () => {
        const hash = window.location.hash.replace('#', '');
        if (views[hash]) switchScreen(hash);
      });

      // Initial route
      const initialHash = window.location.hash.replace('#', '') || 'landing';
      switchScreen(initialHash);

      // Toast helper
      const toast = document.getElementById('desk-toast');
      const toastText = document.getElementById('toast-text');
      let toastTimer = null;

      function showToast(message, duration = 3000) {
        if (!toast || !toastText) return;
        if (toastTimer) clearTimeout(toastTimer);
        toastText.textContent = message;
        toast.classList.add('is-visible');
        toastTimer = setTimeout(() => {
          toast.classList.remove('is-visible');
        }, duration);
      }

      // ----------------------------------------------------------------------
      // 2. MODAL CONTROLLER
      // ----------------------------------------------------------------------
      const infoModal = document.getElementById('info-modal');
      document.getElementById('nav-how-it-works')?.addEventListener('click', () => openModal(infoModal));
      document.getElementById('mobile-how-it-works')?.addEventListener('click', () => {
        mobileNavPanel?.classList.remove('is-open');
        openModal(infoModal);
      });
      document.getElementById('hero-explore-how-it-works')?.addEventListener('click', () => openModal(infoModal));
      document.getElementById('rail-help-btn')?.addEventListener('click', () => openModal(infoModal));

      function openModal(modal) {
        if (!modal) return;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
      }

      function closeModal(modal) {
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
      }

      document.querySelectorAll('[data-close-modal]').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.getAttribute('data-close-modal');
          closeModal(document.getElementById(id));
        });
      });

      document.querySelectorAll('.modal-backdrop').forEach(bd => {
        bd.addEventListener('click', (e) => {
          if (e.target === bd) closeModal(bd);
        });
      });

      // ----------------------------------------------------------------------
      // 3. LANDING PAGE INTERACTIONS
      // ----------------------------------------------------------------------
      const btnToggleSwitch = document.getElementById('btn-toggle-switch');
      const switchArm = document.getElementById('switch-arm');
      const switchGroup = document.getElementById('circuit-switch-group');
      const bulbGlow = document.getElementById('bulb-glow');
      const switchDot = document.getElementById('switch-dot');
      const circuitStatusText = document.getElementById('circuit-status-text');
      const circuitArrows = document.querySelectorAll('.circuit-arrow');
      let isSwitchClosed = true;

      btnToggleSwitch?.addEventListener('click', () => {
        isSwitchClosed = !isSwitchClosed;
        const label = switchGroup?.querySelector('text');

        if (isSwitchClosed) {
          switchArm?.setAttribute('x2', '23');
          switchArm?.setAttribute('y2', '0');
          if (label) label.textContent = 'SWITCH (CLOSED)';
          if (bulbGlow) bulbGlow.style.opacity = '0.25';
          if (switchDot) switchDot.style.backgroundColor = '#71886B';
          if (circuitStatusText) circuitStatusText.textContent = 'Continuous loop active • I = 0.9A';
          circuitArrows.forEach(arr => arr.style.display = 'block');
          showToast('Switch closed: electrons flowing smoothly.');
        } else {
          switchArm?.setAttribute('x2', '10');
          switchArm?.setAttribute('y2', '-22');
          if (label) label.textContent = 'SWITCH (OPEN)';
          if (bulbGlow) bulbGlow.style.opacity = '0';
          if (switchDot) switchDot.style.backgroundColor = '#B86D52';
          if (circuitStatusText) circuitStatusText.textContent = 'Circuit broken • Current I = 0A';
          circuitArrows.forEach(arr => arr.style.display = 'none');
          showToast('Switch opened: current drops to 0A.');
        }
      });

      // Landing question checkpoint
      const optionButtons = document.querySelectorAll('#question-card .option-btn');
      const teacherFeedback = document.getElementById('teacher-feedback');
      const workspaceProgressBar = document.getElementById('workspace-progress-bar');

      optionButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          optionButtons.forEach(b => b.classList.remove('correct', 'incorrect'));
          const correct = btn.getAttribute('data-correct') === 'true';
          const feedback = btn.getAttribute('data-feedback');

          if (correct) {
            btn.classList.add('correct');
            if (teacherFeedback) teacherFeedback.innerHTML = `<strong>Dr. Aris:</strong> "${feedback}"`;
            if (workspaceProgressBar) workspaceProgressBar.style.width = '57%';
            showToast('Correct! Ohm\'s Law mastered.');
          } else {
            btn.classList.add('incorrect');
            if (teacherFeedback) teacherFeedback.innerHTML = `<strong>Dr. Aris:</strong> "${feedback}"`;
            showToast('Try again: remember how resistance opposes current.');
          }
        });
      });

      // Landing Pipeline Nodes
      const pipelineStages = document.querySelectorAll('.pipeline-stage-node');
      const stageDetailsText = document.getElementById('stage-details-text');
      const stageDetailsPill = document.getElementById('stage-details-pill');

      const pipelineTextMap = {
        '1': 'Stage 01 • PDF Ingestion: Drag and drop syllabi, chapters, lecture transcripts, or complex academic papers. The system maps the underlying knowledge graph.',
        '2': 'Stage 02 • Dynamic Lesson Plan: MENTORE decomposes the topic into intuitive cognitive milestones, prioritizing physical intuition and foundational metaphors before formulas.',
        '3': 'Stage 03 • MENTORE Presentation: Synchronized spoken explanation, live blackboard sketches, and self-drawing diagrams bring abstract concepts into tangible clarity.',
        '4': 'Stage 04 • Socratic Checkpoint: Calibrated questions test depth of comprehension rather than rote memory, verifying your intuitive grasp before proceeding.',
        '5': 'Stage 05 • Real-time Adaptation: If an answer shows hesitation or a misunderstanding, the teacher switches analogies, adjusts pacing, and offers tactile examples.',
        '6': 'Stage 06 • Learning Report: Generates an ongoing visual knowledge graph of mastered concepts and schedules spaced-repetition refreshers for permanent retention.'
      };

      pipelineStages.forEach(node => {
        node.addEventListener('click', () => {
          const s = node.getAttribute('data-stage');
          pipelineStages.forEach(n => n.classList.remove('is-active'));
          node.classList.add('is-active');
          if (stageDetailsText && pipelineTextMap[s]) {
            stageDetailsText.innerHTML = `<strong>${pipelineTextMap[s].split(':')[0]}:</strong>${pipelineTextMap[s].split(':')[1]}`;
          }
          if (stageDetailsPill) stageDetailsPill.textContent = `Step ${s} of 6`;
        });
      });

      // ----------------------------------------------------------------------
      // 4. ONBOARDING SCREEN
      // ----------------------------------------------------------------------
      function bindSingleSelectChips(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        const chips = container.querySelectorAll('.choice-chip');
        chips.forEach(chip => {
          chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('is-selected'));
            chip.classList.add('is-selected');
          });
        });
      }

      bindSingleSelectChips('level-chips');
      bindSingleSelectChips('language-chips');
      bindSingleSelectChips('goal-chips');

      const onboardingForm = document.getElementById('onboarding-form');
      const studentNameInput = document.getElementById('student-name-input');
      const dashUserNameDisplay = document.getElementById('dash-user-name-display');
      const dashAvatarDisplay = document.getElementById('dash-avatar-display');

      onboardingForm?.addEventListener('submit', () => {
        const name = studentNameInput?.value.trim() || 'Maya Patel';
        if (dashUserNameDisplay) dashUserNameDisplay.textContent = name;
        if (dashAvatarDisplay) dashAvatarDisplay.textContent = name.charAt(0).toUpperCase();

        showToast(`Welcome, ${name}! Your personalized learning space is ready.`);
        window.location.hash = 'dashboard';
        switchScreen('dashboard');
      });

      // ----------------------------------------------------------------------
      // 5. DASHBOARD SCREEN
      // ----------------------------------------------------------------------
      const dashQuickTopic = document.getElementById('dash-quick-topic');
      const btnDashQuickSubmit = document.getElementById('btn-dash-quick-submit');
      const createTopicTextarea = document.getElementById('create-topic-textarea');

      function handleDashTopicSearch() {
        const query = dashQuickTopic?.value.trim();
        if (query && createTopicTextarea) {
          createTopicTextarea.value = query;
        }
        window.location.hash = 'create-lesson';
        switchScreen('create-lesson');
      }

      btnDashQuickSubmit?.addEventListener('click', handleDashTopicSearch);
      dashQuickTopic?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleDashTopicSearch();
      });

      document.getElementById('dash-notif-btn')?.addEventListener('click', () => {
        showToast('You have 2 learning checkpoint recommendations waiting.');
      });

      // ----------------------------------------------------------------------
      // 6. CREATE A LESSON SCREEN
      // ----------------------------------------------------------------------
      bindSingleSelectChips('create-level-chips');
      bindSingleSelectChips('create-time-chips');
      bindSingleSelectChips('create-lang-chips');

      const createPaperDropzone = document.getElementById('create-paper-dropzone');
      const createFileInput = document.getElementById('create-file-input');

      createPaperDropzone?.addEventListener('click', () => createFileInput?.click());
      createFileInput?.addEventListener('change', async (e) => {
        if (e.target.files && e.target.files[0]) {
          const file = e.target.files[0];
          createPaperDropzone.innerHTML = `
            <div class="paper-dropzone-icon" style="background-color: var(--color-moss-light); color: var(--color-moss);">
              ⌛
            </div>
            <p class="paper-drop-main-text" style="color: var(--color-charcoal); font-weight: 600;">Ingesting & Chunking: ${file.name}...</p>
            <span class="paper-drop-formats">PyMuPDF semantic sectioning in progress...</span>
          `;
          
          try {
            const formData = new FormData();
            formData.append('file', file);
            const uploadResp = await fetch('http://localhost:8000/api/v1/documents/upload', {
              method: 'POST',
              body: formData
            });
            if (uploadResp.ok) {
              const uploadData = await uploadResp.json();
              createPaperDropzone.innerHTML = `
                <div class="paper-dropzone-icon" style="background-color: var(--color-moss-light); color: var(--color-moss);">
                  ✓
                </div>
                <p class="paper-drop-main-text" style="color: var(--color-moss); font-weight: 600;">${file.name}</p>
                <span class="paper-drop-formats">${(file.size / (1024 * 1024)).toFixed(2)} MB • Ingested ${uploadData.total_chunks || 12} semantic chunks</span>
              `;
              showToast(`Uploaded & indexed ${file.name} into Knowledge Graph.`);
              loadDynamicLibraryDocs();
              return;
            }
          } catch (err) {
            console.warn('Upload fallback active:', err);
          }

          createPaperDropzone.innerHTML = `
            <div class="paper-dropzone-icon" style="background-color: var(--color-moss-light); color: var(--color-moss);">
              ✓
            </div>
            <p class="paper-drop-main-text" style="color: var(--color-moss); font-weight: 600;">${file.name}</p>
            <span class="paper-drop-formats">${(file.size / (1024 * 1024)).toFixed(2)} MB • Ingestion complete</span>
          `;
          showToast(`Ingested file: ${file.name}`);
        }
      });

      async function loadDynamicLibraryDocs() {
        const listEl = document.getElementById('library-docs-list');
        if (!listEl) return;
        try {
          const resp = await fetch('http://localhost:8000/api/v1/documents');
          if (resp.ok) {
            const data = await resp.json();
            if (data.documents && data.documents.length > 0) {
              listEl.innerHTML = '';
              data.documents.forEach(doc => {
                const row = document.createElement('div');
                row.className = 'doc-row-item';
                row.innerHTML = `
                  <div class="doc-row-left">
                    <div class="doc-paper-thumbnail">${(doc.file_type || 'PDF').toUpperCase()}</div>
                    <div>
                      <h4 style="font-size: 1rem; font-weight: 600; color: #29251F;">${doc.filename}</h4>
                      <span style="font-size: 0.8125rem; color: #766E63;">${(doc.file_type || 'PDF').toUpperCase()} • ${doc.total_chapters || 8} chapters • Last studied ${doc.last_studied || 'Today'}</span>
                    </div>
                  </div>
                  <span style="font-size: 0.875rem; color: #B86D52; font-weight: 600;">Open lesson →</span>
                `;
                row.addEventListener('click', () => {
                  window.location.hash = 'player';
                  switchScreen('player');
                });
                listEl.appendChild(row);
              });
            }
          }
        } catch (e) {}
      }

      const btnBuildLesson = document.getElementById('btn-build-lesson');
      const btnBuildLessonText = document.getElementById('btn-build-lesson-text');
      const btnProgressLine = document.getElementById('btn-progress-line');

      window.activeAILessonPlan = null;

      btnBuildLesson?.addEventListener('click', async () => {
        const topic = createTopicTextarea?.value.trim() || 'Understanding Electricity';
        const level = document.querySelector('#create-level-chips .chip.selected')?.textContent.trim().toLowerCase() || 'beginner';
        const durationStr = document.querySelector('#create-time-chips .chip.selected')?.textContent.trim() || '20 min';
        const duration = parseInt(durationStr) || 20;
        const language = document.querySelector('#create-lang-chips .chip.selected')?.textContent.trim() || 'Hinglish';

        if (btnBuildLessonText) btnBuildLessonText.textContent = 'Generating AI curriculum...';
        if (btnProgressLine) btnProgressLine.style.width = '60%';
        btnBuildLesson.style.pointerEvents = 'none';

        try {
          const resp = await fetch('http://localhost:8000/api/v1/lessons/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              topic: topic,
              level: level,
              duration_minutes: duration,
              language: language
            })
          });
          if (resp.ok) {
            window.activeAILessonPlan = await resp.json();
            showToast(`MENTORE generated ${window.activeAILessonPlan.segments?.length || 5} learning segments.`);
          }
        } catch (e) {
          console.warn('Lesson generation fallback active:', e);
        }

        if (btnProgressLine) btnProgressLine.style.width = '100%';
        setTimeout(() => {
          if (btnBuildLessonText) btnBuildLessonText.textContent = 'Build my lesson →';
          if (btnProgressLine) btnProgressLine.style.width = '0%';
          btnBuildLesson.style.pointerEvents = '';

          window.location.hash = 'prep';
          switchScreen('prep');
        }, 800);
      });

      // ----------------------------------------------------------------------
      // 7. CINEMATIC LESSON PREPARATION SCREEN
      // ----------------------------------------------------------------------
      let prepSimulationTimer = null;

      async function runPrepSimulation() {
        if (prepSimulationTimer) clearTimeout(prepSimulationTimer);

        const step4 = document.getElementById('prep-step-4');
        const step5 = document.getElementById('prep-step-5');
        const step6 = document.getElementById('prep-step-6');

        if (step4) {
          step4.className = 'prep-step-item is-active';
          step4.querySelector('.prep-step-icon').textContent = '●';
        }
        if (step5) {
          step5.className = 'prep-step-item is-pending';
          step5.querySelector('.prep-step-icon').textContent = '○';
        }
        if (step6) {
          step6.className = 'prep-step-item is-pending';
          step6.querySelector('.prep-step-icon').textContent = '○';
        }

        try {
          const plan = window.activeAILessonPlan;
          let text = "Welcome to the lesson.";
          if (plan && plan.segments && plan.segments[0]) {
             text = plan.segments[0].caption;
          }
          
          const resp = await fetch('http://localhost:8000/api/v1/media/voice/synthesize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
          });
          const data = await resp.json();
          const jobId = data.job_id;

          const pollInterval = setInterval(async () => {
             try {
               const statResp = await fetch(`http://localhost:8000/api/v1/media/job/${jobId}`);
               const jobStat = await statResp.json();
               
               if (jobStat.stage === 'VISUAL' || jobStat.stage === 'AVATAR') {
                 if (step4) {
                   step4.className = 'prep-step-item is-done';
                   step4.querySelector('.prep-step-icon').textContent = '✓';
                 }
                 if (step5 && step5.className !== 'prep-step-item is-done') {
                   step5.className = 'prep-step-item is-active';
                   step5.querySelector('.prep-step-icon').textContent = '●';
                 }
               }

               if (jobStat.stage === 'COMPOSE' || jobStat.stage === 'UPLOAD' || jobStat.stage === 'READY') {
                 if (step5) {
                   step5.className = 'prep-step-item is-done';
                   step5.querySelector('.prep-step-icon').textContent = '✓';
                 }
                 if (step6 && step6.className !== 'prep-step-item is-done') {
                   step6.className = 'prep-step-item is-active';
                   step6.querySelector('.prep-step-icon').textContent = '●';
                 }
               }

               if (jobStat.status === 'READY') {
                 clearInterval(pollInterval);
                 if (step6) {
                   step6.className = 'prep-step-item is-done';
                   step6.querySelector('.prep-step-icon').textContent = '✓';
                 }
                 showToast('Lesson ready! Video generated successfully.');
                 window.activeVideoUrl = jobStat.video_url;
               } else if (jobStat.status === 'FALLBACK_AUDIO_ONLY') {
                 clearInterval(pollInterval);
                 window.location.hash = 'fallback';
                 switchScreen('fallback');
               }
             } catch (pollErr) {
               console.error("Polling error", pollErr);
             }
          }, 1000);

        } catch (err) {
          console.error("Failed to start media job", err);
          window.location.hash = 'fallback';
          switchScreen('fallback');
        }
      }

      function applyAILessonPlanToPlayer() {
        const plan = window.activeAILessonPlan;
        if (!plan) return;

        const titleEl = document.getElementById('player-lesson-title');
        if (titleEl && plan.topic) titleEl.textContent = plan.topic;

        const seqBar = document.getElementById('player-sequence-bar');
        if (seqBar && plan.segments && plan.segments.length > 0) {
          seqBar.innerHTML = '';
          plan.segments.forEach((seg, idx) => {
            const pill = document.createElement('button');
            pill.type = 'button';
            pill.className = idx === 0 ? 'seq-segment-pill current' : 'seq-segment-pill upcoming';
            pill.setAttribute('data-segment-idx', idx);
            pill.innerHTML = `<span>${seg.concept.toUpperCase()}</span> <span class="seq-pill-icon">${idx === 0 ? '●' : '○'}</span>`;
            
            pill.addEventListener('click', () => {
              // Update pill styles
              seqBar.querySelectorAll('.seq-segment-pill').forEach((p, pIdx) => {
                if (pIdx === idx) {
                  p.className = 'seq-segment-pill current';
                  p.querySelector('.seq-pill-icon').textContent = '●';
                } else if (pIdx < idx) {
                  p.className = 'seq-segment-pill completed';
                  p.querySelector('.seq-pill-icon').textContent = '✓';
                } else {
                  p.className = 'seq-segment-pill upcoming';
                  p.querySelector('.seq-pill-icon').textContent = '○';
                }
              });

              if (playerActiveCaption) {
                playerActiveCaption.style.opacity = '0';
                setTimeout(() => {
                  playerActiveCaption.textContent = `"${seg.caption}"`;
                  playerActiveCaption.style.opacity = '1';
                }, 160);
              }
              if (canvasActiveTitle) canvasActiveTitle.textContent = `${seg.concept}: Visual Model`;
              if (canvasActiveTag) canvasActiveTag.textContent = seg.strategy.toUpperCase();
              showToast(`Now teaching: ${seg.concept}`);
            });

            seqBar.appendChild(pill);
          });

          // Set initial segment caption
          if (playerActiveCaption && plan.segments[0]) {
            playerActiveCaption.textContent = `"${plan.segments[0].caption}"`;
          }
          if (canvasActiveTitle && plan.segments[0]) {
            canvasActiveTitle.textContent = `${plan.segments[0].concept}: Visual Model`;
          }
        }
      }

      document.getElementById('btn-enter-lesson-player')?.addEventListener('click', () => {
        applyAILessonPlanToPlayer();
        window.location.hash = 'player';
        switchScreen('player');
      });

      // ----------------------------------------------------------------------
      // 8. FLAGSHIP LESSON PLAYER & INTERACTIVE CHECKPOINT SYSTEM
      // ----------------------------------------------------------------------
      const playerSequencePills = document.querySelectorAll('#player-sequence-bar .seq-segment-pill');
      const playerActiveCaption = document.getElementById('player-active-caption');
      const canvasActiveTitle = document.getElementById('canvas-active-title');
      const canvasActiveTag = document.getElementById('canvas-active-tag');
      const playerCanvasFocus = document.getElementById('player-canvas-dynamic-focus');
      const playerBtnPlay = document.getElementById('player-btn-play');
      const playerTeacherState = document.getElementById('player-teacher-state');
      const playerTeacherFrame = document.getElementById('player-teacher-frame');
      let isPlaying = true;

      const segmentData = {
        'intro': {
          title: 'Foundational Baseline: What is Electricity?',
          tag: 'Conceptual Intro',
          caption: '"Sit down comfortably. Before we write any formulas, think about what happens when you turn a flashlight switch."',
          focusBox: 'CLOSED SYSTEM (LOOP)'
        },
        'current': {
          title: 'Current Flow: Coulombs Passing per Second',
          tag: 'Rate of Charge (I = Q / t)',
          caption: '"Electric current is simply the orderly drift of charge carriers along a conductor over time."',
          focusBox: 'ELECTRON DRIFT (I)'
        },
        'voltage': {
          title: 'Visual Model: Voltage as Electric Pressure',
          tag: 'Potential Difference (ΔV)',
          caption: '"Voltage is the force that pushes electrical charge through a circuit."',
          focusBox: 'HIGH POTENTIAL (+)'
        },
        'resistance': {
          title: 'Resistance: Material Opposition & Thermal Dissipation',
          tag: 'Ohmic Friction (R)',
          caption: '"Resistance measures how strongly a material resists current flow, turning electrical energy into light and warmth."',
          focusBox: 'COLLISION IMPEDANCE (R)'
        },
        'ohms-law': {
          title: 'The Unifying Law: V = I × R Equilibrium',
          tag: 'Mathematical Relationship',
          caption: '"Ohm\'s Law links pressure, flow rate, and friction: double the resistance at constant voltage, and current is cut in half."',
          focusBox: 'V = I × R FORMULA'
        }
      };

      playerSequencePills.forEach(pill => {
        pill.addEventListener('click', () => {
          const segKey = pill.getAttribute('data-segment');
          const data = segmentData[segKey];
          if (!data) return;

          let foundCurrent = false;
          playerSequencePills.forEach(p => {
            const k = p.getAttribute('data-segment');
            if (k === segKey) {
              p.className = 'seq-segment-pill current';
              p.children[1].textContent = '●';
              foundCurrent = true;
            } else if (!foundCurrent) {
              p.className = 'seq-segment-pill completed';
              p.children[1].textContent = '✓';
            } else {
              p.className = 'seq-segment-pill upcoming';
              p.children[1].textContent = '○';
            }
          });

          if (playerActiveCaption) {
            playerActiveCaption.style.opacity = '0';
            setTimeout(() => {
              playerActiveCaption.textContent = data.caption;
              playerActiveCaption.style.opacity = '1';
            }, 180);
          }

          if (canvasActiveTitle) canvasActiveTitle.textContent = data.title;
          if (canvasActiveTag) canvasActiveTag.textContent = data.tag;

          const focusText = playerCanvasFocus?.querySelector('text');
          if (focusText) focusText.textContent = data.focusBox;

          showToast(`Now discussing: ${segKey.toUpperCase()}`);
        });
      });

      playerBtnPlay?.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          playerBtnPlay.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>';
          if (playerTeacherState) playerTeacherState.textContent = 'Dr. Aris is explaining...';
          playerTeacherFrame?.classList.add('is-speaking');
          showToast('Lesson resumed.');
        } else {
          playerBtnPlay.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>';
          if (playerTeacherState) playerTeacherState.textContent = 'Paused • Teacher is ready';
          playerTeacherFrame?.classList.remove('is-speaking');
          showToast('Lesson paused.');
        }
      });

      document.getElementById('player-btn-replay')?.addEventListener('click', () => {
        showToast('Replaying last 10 seconds of explanation.');
      });

      const captionsBtn = document.getElementById('player-btn-captions');
      let captionsOn = true;
      captionsBtn?.addEventListener('click', () => {
        captionsOn = !captionsOn;
        if (captionsBtn) captionsBtn.textContent = captionsOn ? 'CC ON' : 'CC OFF';
        const box = document.querySelector('.player-caption-box');
        if (box) box.style.opacity = captionsOn ? '1' : '0.2';
      });

      // Multilingual Language Switcher (Hinglish -> Hindi -> English -> Hinglish)
      const langBtn = document.getElementById('player-btn-lang');
      const languagesList = ['Hinglish', 'Hindi', 'English'];
      let currentLangIndex = 0;

      langBtn?.addEventListener('click', async () => {
        currentLangIndex = (currentLangIndex + 1) % languagesList.length;
        const newLang = languagesList[currentLangIndex];
        if (langBtn) langBtn.textContent = newLang;

        // Fetch live translation from FastAPI backend
        try {
          const resp = await fetch('http://localhost:8000/api/v1/teaching/language/switch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ concept: 'voltage', target_language: newLang })
          });
          if (resp.ok) {
            const data = await resp.json();
            if (playerActiveCaption) {
              playerActiveCaption.style.opacity = '0';
              setTimeout(() => {
                playerActiveCaption.textContent = data.caption;
                playerActiveCaption.style.opacity = '1';
              }, 160);
            }
            if (canvasActiveTitle) canvasActiveTitle.textContent = data.title;
            if (playerTeacherState) playerTeacherState.textContent = data.status;
            showToast(`Teacher language switched to: ${newLang}`);
            return;
          }
        } catch (e) {}

        showToast(`Language switched to: ${newLang}`);
      });

      function startPlayerSimulation() {
        showToast('Classroom active. Sitting inside quiet modern study desk.', 3500);
      }

      // ----------------------------------------------------------------------
      // CHECKPOINT SUB-STATES: EVALUATION, CORRECT & ADAPTIVE RE-EXPLAIN
      // ----------------------------------------------------------------------
      const checkpointOverlay = document.getElementById('player-checkpoint-overlay');
      const checkpointStateQuestion = document.getElementById('checkpoint-state-question');
      const checkpointStateCorrect = document.getElementById('checkpoint-state-correct');
      const checkpointStateMisconception = document.getElementById('checkpoint-state-misconception');
      const btnCheckAnswer = document.getElementById('btn-check-checkpoint-answer');
      const checkpointChoiceBtns = document.querySelectorAll('.checkpoint-choice-btn');
      let selectedCheckpointChoice = 'B'; // default to correct or let user choose

      function openCheckpoint() {
        if (!checkpointOverlay) return;
        // Pause teacher video
        isPlaying = false;
        if (playerBtnPlay) playerBtnPlay.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>';
        if (playerTeacherState) playerTeacherState.textContent = 'Paused for Quick Check';
        playerTeacherFrame?.classList.remove('is-speaking');

        // Reset to question view
        checkpointStateQuestion.style.display = 'block';
        checkpointStateCorrect.classList.remove('active');
        checkpointStateMisconception.classList.remove('active');
        checkpointOverlay.classList.add('active');
        showToast('Quick check: Your teacher paused to verify understanding.');
      }

      document.getElementById('btn-trigger-checkpoint')?.addEventListener('click', openCheckpoint);
      document.getElementById('btn-quick-checkpoint')?.addEventListener('click', () => {
        window.location.hash = 'player';
        switchScreen('player');
        setTimeout(openCheckpoint, 300);
      });

      checkpointChoiceBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          checkpointChoiceBtns.forEach(b => b.classList.remove('selected'));
          btn.classList.add('selected');
          selectedCheckpointChoice = btn.getAttribute('data-choice');
        });
      });

      btnCheckAnswer?.addEventListener('click', async () => {
        checkpointStateQuestion.style.display = 'none';

        // Query Live FastAPI Backend
        try {
          const resp = await fetch('http://localhost:8000/api/v1/teaching/checkpoint/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ choice: selectedCheckpointChoice, concept: 'Resistance' })
          });
          if (resp.ok) {
            const data = await resp.json();
            if (data.is_correct) {
              checkpointStateCorrect.classList.add('active');
              showToast('Exactly! Evaluated by AI Teaching Engine.');
            } else {
              checkpointStateMisconception.classList.add('active');
              showToast(`Misconception diagnosed: ${data.misconception_category}`);
              const brainDecisionVal = document.querySelector('.brain-decision-val');
              if (brainDecisionVal) brainDecisionVal.textContent = 'ADAPTIVE INTERVENTION';
            }
            return;
          }
        } catch (e) {
          // Graceful fallback if offline
        }

        if (selectedCheckpointChoice === 'B') {
          // CORRECT ANSWER STATE
          checkpointStateCorrect.classList.add('active');
          showToast('Exactly! Resistance restricts current flow.');

          // Animate mastery number 68% -> 78%
          const masteryPill = document.getElementById('mastery-display-pill');
          let m = 68;
          const countTimer = setInterval(() => {
            m += 2;
            if (m >= 78) {
              m = 78;
              clearInterval(countTimer);
            }
            if (masteryPill) masteryPill.textContent = `Resistance ${m}% → 78%`;
          }, 60);

        } else {
          // ADAPTIVE TEACHING STATE (Misconception: Inverse relationship reversed)
          checkpointStateMisconception.classList.add('active');
          showToast('Misconception noted: Teacher adapting explanation...');

          // Update Teacher Brain Drawer with this live event
          const brainDecisionVal = document.querySelector('.brain-decision-val');
          if (brainDecisionVal) brainDecisionVal.textContent = 'ADAPTIVE INTERVENTION';
        }
      });

      // Continue after correct answer -> Final Assessment
      document.getElementById('btn-correct-continue')?.addEventListener('click', () => {
        checkpointOverlay.classList.remove('active');
        showToast('Moving forward to Final Mastery Assessment...');
        window.location.hash = 'assessment';
        switchScreen('assessment');
      });

      // Try different explanation (Water-pipe analogy)
      document.getElementById('btn-try-waterpipe-analogy')?.addEventListener('click', () => {
        checkpointOverlay.classList.remove('active');

        // Dynamically replace visual canvas with Water Pipe diagram
        const mount = document.getElementById('canvas-svg-mount');
        if (mount) {
          mount.innerHTML = `
            <svg class="player-svg-interactive" viewBox="0 0 460 210" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="2" width="456" height="206" rx="8" fill="#FFFDF9" stroke="#B86D52" />
              <!-- Wide Pipe (Low Resistance, High Flow) -->
              <rect x="50" y="45" width="160" height="40" rx="4" fill="#EBF1EA" stroke="#71886B" stroke-width="1.8" />
              <text x="130" y="68" font-family="'JetBrains Mono', monospace" font-size="11" fill="#71886B" font-weight="600" text-anchor="middle">WIDE PIPE: FAST FLOW</text>
              
              <!-- Narrow Constriction Pipe (High Resistance, Reduced Flow) -->
              <rect x="250" y="55" width="160" height="20" rx="4" fill="#F7E9E4" stroke="#B86D52" stroke-width="1.8" />
              <text x="330" y="68" font-family="'JetBrains Mono', monospace" font-size="11" fill="#B86D52" font-weight="600" text-anchor="middle">NARROW: CONSTRICTED</text>

              <!-- Water Wave Particles -->
              <path d="M 60 65 Q 100 60 140 65 T 200 65" stroke="#71886B" stroke-width="2.5" />
              <path d="M 260 65 Q 300 62 340 65 T 400 65" stroke="#B86D52" stroke-width="1.5" />

              <text x="130" y="115" font-family="'Fraunces', serif" font-size="12" fill="#29251F" text-anchor="middle">Low Resistance = High Current</text>
              <text x="330" y="115" font-family="'Fraunces', serif" font-size="12" fill="#29251F" text-anchor="middle">High Resistance = Restricted Current</text>
            </svg>
          `;
        }

        if (canvasActiveTitle) canvasActiveTitle.textContent = 'Alternative Model: Water-Pipe Analogy';
        if (canvasActiveTag) canvasActiveTag.textContent = 'Hydraulic Metaphor';
        if (playerActiveCaption) {
          playerActiveCaption.textContent = '"Think of resistance as narrowing a water pipe: with the same pressure, fewer gallons flow per minute. That is why current must drop."';
        }
        showToast('Dr. Aris switched to the Water-Pipe analogy.');
      });

      // ----------------------------------------------------------------------
      // 9. TEACHER BRAIN SIDE INSPECTOR
      // ----------------------------------------------------------------------
      const teacherBrainDrawer = document.getElementById('teacher-brain-drawer');
      async function toggleTeacherBrain(forceState) {
        if (!teacherBrainDrawer) return;
        const open = typeof forceState === 'boolean' ? forceState : !teacherBrainDrawer.classList.contains('open');
        if (open) {
          teacherBrainDrawer.classList.add('open');
          // Fetch live from FastAPI backend
          try {
            const resp = await fetch('http://localhost:8000/api/v1/teaching/brain-inspect');
            if (resp.ok) {
              const data = await resp.json();
              const decisionVal = teacherBrainDrawer.querySelector('.brain-decision-val');
              if (decisionVal) decisionVal.textContent = data.decision;
            }
          } catch (e) {}
          showToast('Teacher Brain Inspector open: viewing real-time pedagogical decisions.');
        } else {
          teacherBrainDrawer.classList.remove('open');
        }
      }

      document.getElementById('btn-toggle-teacher-brain')?.addEventListener('click', () => toggleTeacherBrain());
      document.getElementById('btn-close-teacher-brain')?.addEventListener('click', () => toggleTeacherBrain(false));
      document.getElementById('btn-quick-brain')?.addEventListener('click', () => toggleTeacherBrain());

      // Natural Academic Speech Synthesizer
      function speakTeacherCaption(text, lang = 'en-US') {
        if (!('speechSynthesis' in window)) return;
        try {
          window.speechSynthesis.cancel();
          if (!isPlaying) return;

          const cleanText = text.replace(/["']/g, '').trim();
          if (!cleanText) return;

          const utterance = new SpeechSynthesisUtterance(cleanText);
          utterance.rate = 0.95; // Calm academic cadence
          utterance.pitch = 1.0;

          if (lang.includes('Hindi') || lang.includes('Hinglish')) {
            utterance.lang = 'hi-IN';
          } else {
            utterance.lang = 'en-US';
          }

          utterance.onstart = () => {
            playerTeacherFrame?.classList.add('is-speaking');
          };
          utterance.onend = () => {
            if (!isPlaying) playerTeacherFrame?.classList.remove('is-speaking');
          };
          utterance.onerror = () => {
            // Graceful silent fallback
          };

          window.speechSynthesis.speak(utterance);
        } catch (e) {}
      }

      // ----------------------------------------------------------------------
      // 10. CONTEXTUAL "ASK YOUR TEACHER" DOCK
      // ----------------------------------------------------------------------
      const askDialogBubble = document.getElementById('ask-dialog-bubble');
      document.getElementById('btn-toggle-ask-dock')?.addEventListener('click', () => {
        if (askDialogBubble) {
          askDialogBubble.classList.toggle('open');
        }
      });

      document.getElementById('ask-act-explain')?.addEventListener('click', async () => {
        showToast('Consulting Dr. Aris via AI Teaching Engine...');
        try {
          const resp = await fetch('http://localhost:8000/api/v1/teaching/contextual-ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: 'Explain with physical intuition', concept: 'Resistance' })
          });
          if (resp.ok) {
            const data = await resp.json();
            showToast(`Dr. Aris: "${data.teacher_response}"`, 5000);
            speakTeacherCaption(data.teacher_response);
            if (askDialogBubble) askDialogBubble.classList.remove('open');
            return;
          }
        } catch (e) {}
        showToast('Dr. Aris: Rephrasing using physical intuition.');
        if (askDialogBubble) askDialogBubble.classList.remove('open');
      });

      document.getElementById('ask-act-example')?.addEventListener('click', async () => {
        showToast('Dr. Aris: "Think of resistance as narrowing a water pipe: with the same water pressure, fewer gallons pass per minute."', 5000);
        speakTeacherCaption('Think of resistance as narrowing a water pipe: with the same water pressure, fewer gallons pass per minute.');
        if (askDialogBubble) askDialogBubble.classList.remove('open');
      });

      document.getElementById('ask-act-question')?.addEventListener('click', () => {
        if (askDialogBubble) askDialogBubble.classList.remove('open');
        openCheckpoint();
      });

      // ----------------------------------------------------------------------
      // 11. FINAL ASSESSMENT SCREEN
      // ----------------------------------------------------------------------
      let currentAssessIndex = 3; // Question 3 of 8
      const assessCounterText = document.getElementById('assess-counter-text');
      const assessDotsContainer = document.getElementById('assess-dots-container');

      document.getElementById('btn-assess-submit')?.addEventListener('click', async () => {
        currentAssessIndex++;
        if (currentAssessIndex > 8) {
          // Assessment complete -> Query live FastAPI grading endpoint
          showToast('Assessment finished! Generating your personalized learning report from AI Engine...');
          try {
            const resp = await fetch('http://localhost:8000/api/v1/assessment/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ student_answers: { q1: 'B', q2: 'A', q3: 'C', q4: 'B', q5: 'B', q6: 'C', q7: 'A', q8: 'B' } })
            });
            if (resp.ok) {
              const report = await resp.json();
              const scoreEl = document.querySelector('.report-big-score');
              if (scoreEl) scoreEl.textContent = `${report.score_pct}%`;
              const noteEl = document.querySelector('.teacher-note-bubble p');
              if (noteEl) noteEl.textContent = `"${report.teacher_observation}"`;
            }
          } catch (e) {}

          window.location.hash = 'report';
          switchScreen('report');
        } else {
          if (assessCounterText) assessCounterText.textContent = `Question ${currentAssessIndex} of 8`;
          // Update dots
          if (assessDotsContainer) {
            const dots = assessDotsContainer.querySelectorAll('.assess-dot');
            dots.forEach((d, idx) => {
              if (idx < currentAssessIndex - 1) {
                d.className = 'assess-dot answered';
              } else if (idx === currentAssessIndex - 1) {
                d.className = 'assess-dot current';
              } else {
                d.className = 'assess-dot';
              }
            });
          }
          showToast(`Answer recorded. Advancing to Question ${currentAssessIndex} of 8.`);
        }
      });

      // ----------------------------------------------------------------------
      // 12. PERSONALIZED LEARNING PATH SCREEN
      // ----------------------------------------------------------------------
      const pathNodes = document.querySelectorAll('.path-tree-node');
      const pathPopTitle = document.getElementById('path-pop-title');
      const pathPopMastery = document.getElementById('path-pop-mastery');
      const pathPopDesc = document.getElementById('path-pop-desc');

      const pathDataMap = {
        'foundations': { title: 'Foundations & Atomic Charge', mastery: '98% mastery', desc: 'Coulomb\'s Law, atomic shell structures, and static electricity.' },
        'current': { title: 'Electric Current (I)', mastery: '91% mastery', desc: 'Rate of charge flow, coulombs per second, and drift speed.' },
        'voltage': { title: 'Voltage & Potential Difference', mastery: '84% mastery', desc: 'Electromotive force and potential energy gradients.' },
        'resistance': { title: 'Resistance & Material Impedance', mastery: '42% mastery', desc: '2 concepts understood · 1 misconception detected (inverse current relationship).' },
        'ohms-law': { title: 'Ohm\'s Law Unified Equations', mastery: '38% mastery', desc: 'Upcoming targeted practice.' },
        'circuit-analysis': { title: 'Circuit Topologies & Kirchhoff', mastery: 'Locked', desc: 'Series and parallel branching.' },
        'applications': { title: 'Real-world Practical Applications', mastery: 'Locked', desc: 'Sensors, microchips, and power grids.' }
      };

      pathNodes.forEach(node => {
        node.addEventListener('click', () => {
          pathNodes.forEach(n => n.classList.remove('current'));
          node.classList.add('current');
          const key = node.getAttribute('data-path-node');
          const data = pathDataMap[key];
          if (data) {
            if (pathPopTitle) pathPopTitle.textContent = data.title;
            if (pathPopMastery) pathPopMastery.textContent = data.mastery;
            if (pathPopDesc) pathPopDesc.textContent = data.desc;
            showToast(`Selected path node: ${data.title}`);
          }
        });
      });

      // ----------------------------------------------------------------------
      // 13. TARGETED REVISION SPRINT & ADVANCED FEATURES
      // ----------------------------------------------------------------------
      document.getElementById('btn-start-targeted-revision')?.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();

        showToast('Initiating 5-minute targeted revision sprint from AI Engine...');
        try {
          const resp = await fetch('http://localhost:8000/api/v1/advanced/revision', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: "Ohm's Law" })
          });
          if (resp.ok) {
            const sprint = await resp.json();
            // Switch to player screen
            window.location.hash = 'player';
            switchScreen('player');

            // Set visual to water pipe
            const mount = document.getElementById('canvas-svg-mount');
            if (mount) {
              mount.innerHTML = `
                <svg class="player-svg-interactive" viewBox="0 0 460 210" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="2" y="2" width="456" height="206" rx="8" fill="#FFFDF9" stroke="#B86D52" />
                  <rect x="50" y="45" width="160" height="40" rx="4" fill="#EBF1EA" stroke="#71886B" stroke-width="1.8" />
                  <text x="130" y="68" font-family="'JetBrains Mono', monospace" font-size="11" fill="#71886B" font-weight="600" text-anchor="middle">WIDE: LOW RESISTANCE</text>
                  <rect x="250" y="55" width="160" height="20" rx="4" fill="#F7E9E4" stroke="#B86D52" stroke-width="1.8" />
                  <text x="330" y="68" font-family="'JetBrains Mono', monospace" font-size="11" fill="#B86D52" font-weight="600" text-anchor="middle">NARROW: HIGH RESISTANCE</text>
                  <path d="M 60 65 Q 100 60 140 65 T 200 65" stroke="#71886B" stroke-width="2.5" />
                  <path d="M 260 65 Q 300 62 340 65 T 400 65" stroke="#B86D52" stroke-width="1.5" />
                  <text x="230" y="145" font-family="'Fraunces', serif" font-size="14" fill="#29251F" text-anchor="middle">Targeted Sprint: ${sprint.strategy}</text>
                </svg>
              `;
            }
            if (canvasActiveTitle) canvasActiveTitle.textContent = 'Revision Sprint: Resolving Misconception';
            if (canvasActiveTag) canvasActiveTag.textContent = '5-Minute Focus';
            if (playerActiveCaption) playerActiveCaption.textContent = `"${sprint.script}"`;
            showToast('Sprint active: Water-pipe tactile demonstration.');
            return;
          }
        } catch (err) {}

        window.location.hash = 'player';
        switchScreen('player');
      });

      // ----------------------------------------------------------------------
      // 14. MATERIAL LIBRARY SEARCH
      // ----------------------------------------------------------------------
      const librarySearch = document.getElementById('library-search');
      librarySearch?.addEventListener('input', () => {
        const query = librarySearch.value.toLowerCase().trim();
        document.querySelectorAll('.doc-row-item').forEach(item => {
          const text = item.textContent.toLowerCase();
          item.style.display = text.includes(query) ? 'flex' : 'none';
        });
      });

    } catch (err) {
      console.warn('MENTORE Suite engine initialization notice:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSuite);
  } else {
    initSuite();
  }
})();
