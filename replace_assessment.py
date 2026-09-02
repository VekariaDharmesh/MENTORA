import sys

with open('frontend/app.js', 'r') as f:
    content = f.read()

start_marker = "// 11. FINAL ASSESSMENT SCREEN"
end_marker = "// 12. PERSONALIZED LEARNING PATH SCREEN"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    new_logic = """// 11. FINAL ASSESSMENT SCREEN
      // ----------------------------------------------------------------------
      let currentAssessIndex = 0;
      let assessmentData = null;
      let studentAnswers = {};
      const assessCounterText = document.getElementById('assess-counter-text');
      const assessDotsContainer = document.getElementById('assess-dots-container');
      const assessQuestionTitle = document.getElementById('assess-question-title');
      const assessOptionsList = document.getElementById('assess-options-list');

      window.loadAssessment = async function(topic) {
        showToast('Generating AI Assessment...');
        const resp = await fetch(`http://localhost:8000/api/v1/assessment/generate?topic=${encodeURIComponent(topic)}`);
        if (resp.ok) {
            assessmentData = await resp.json();
            currentAssessIndex = 0;
            studentAnswers = {};
            renderAssessmentQuestion();
        }
      };

      function renderAssessmentQuestion() {
        if (!assessmentData || !assessmentData.questions || currentAssessIndex >= assessmentData.questions.length) return;
        
        const q = assessmentData.questions[currentAssessIndex];
        const total = assessmentData.total_questions;
        
        if (assessCounterText) assessCounterText.textContent = `Question ${currentAssessIndex + 1} of ${total}`;
        
        if (assessDotsContainer) {
            let dotsHtml = '';
            for(let i=0; i<total; i++) {
                if (i < currentAssessIndex) dotsHtml += '<span class="assess-dot answered"></span>';
                else if (i === currentAssessIndex) dotsHtml += '<span class="assess-dot current"></span>';
                else dotsHtml += '<span class="assess-dot"></span>';
            }
            assessDotsContainer.innerHTML = dotsHtml;
        }
        
        if (assessQuestionTitle) assessQuestionTitle.textContent = q.prompt;
        
        if (assessOptionsList) {
            let optsHtml = '';
            for (const [key, val] of Object.entries(q.options)) {
                optsHtml += `
                  <button type="button" class="checkpoint-choice-btn" data-choice="${key}" onclick="selectAssessOption(this)">
                    <span class="checkpoint-choice-key">${key}</span>
                    <span>${val}</span>
                  </button>
                `;
            }
            assessOptionsList.innerHTML = optsHtml;
        }
      }

      window.selectAssessOption = function(btn) {
        document.querySelectorAll('#assess-options-list .checkpoint-choice-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
      };

      document.getElementById('btn-assess-submit')?.addEventListener('click', async () => {
        if (!assessmentData) return;
        
        const selectedBtn = document.querySelector('#assess-options-list .checkpoint-choice-btn.selected');
        if (!selectedBtn) {
            showToast('Please select an option');
            return;
        }
        
        const qId = assessmentData.questions[currentAssessIndex].id;
        studentAnswers[qId] = selectedBtn.getAttribute('data-choice');
        
        currentAssessIndex++;
        if (currentAssessIndex >= assessmentData.questions.length) {
          showToast('Assessment finished! Generating your personalized learning report from AI Engine...');
          try {
            const resp = await fetch('http://localhost:8000/api/v1/assessment/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ student_answers: studentAnswers })
            });
            if (resp.ok) {
              const report = await resp.json();
              const scoreEl = document.querySelector('.report-big-score');
              if (scoreEl) scoreEl.textContent = `${report.score_pct}%`;
              const noteEl = document.querySelector('.teacher-note-bubble p');
              if (noteEl) noteEl.textContent = `"${report.teacher_observation}"`;
              
              const strList = document.querySelector('#report-strong-list');
              if (strList && report.strong_areas) {
                strList.innerHTML = report.strong_areas.map(s => `<li><span class="report-li-dot"></span>${s}</li>`).join('');
              }
              const weakList = document.querySelector('#report-weak-list');
              if (weakList && report.needs_practice) {
                weakList.innerHTML = report.needs_practice.map(s => `<li><span class="report-li-dot" style="background:#B86D52;"></span>${s}</li>`).join('');
              }
            }
          } catch (e) {
            console.error(e);
          }

          window.location.hash = 'report';
          switchScreen('report');
        } else {
          renderAssessmentQuestion();
        }
      });

      // """
    
    new_content = content[:start_idx] + new_logic + content[end_idx:]
    with open('frontend/app.js', 'w') as f:
        f.write(new_content)
    print("Replaced!")
else:
    print("Markers not found.")
