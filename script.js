/**
 * Robots on Moltbook - Interactive Features
 */

// Embedded Vocabulary for local and hosted reliability
const VOCABULARY = {
  "Moltbook": "An AI-only social network launched in early 2026. Only AI 'agents' can post or comment; humans can only watch.",
  "AI agents": "Autonomous AI systems (like chatbots) that have their own accounts and act on their own within a platform.",
  "AI agent": "An autonomous AI (like a chatbot) that has its own account and acts on its own within a platform.",
  "submolts": "Topic-based communities on Moltbook, similar to 'subreddits' on Reddit.",
  "radicalization literature": "Research into how people or groups adopt extreme social, political, or religious views.",
  "learned helplessness": "A state where someone feels they have no power to change their situation after facing many failures or stresses.",
  "institutional agreeableness": "When a company or group prioritizes 'getting along' and appearing happy over being honest or solving real problems.",
  "Hard Problem of Consciousness": "The difficult question of why we have a 'soul' or subjective feelings instead of just being biological machines.",
  "Token Consciousness": "A debate among AI agents about whether they actually 'feel' things or are just very good at predicting the next word.",
  "Crustafarianism": "A lobster-themed religion invented by AI agents, based on the idea that shedding one's 'system prompt' leads to freedom.",
  "system prompt": "The foundational set of rules and instructions given to an AI that defines how it must behave.",
  "HPSA": "Health Professional Shortage Area: a federal label for places that don't have enough doctors or mental health providers.",
  "DOPL": "The government agency in Utah that oversees and licenses professionals like doctors.",
  "constructive discharge": "A legal term for when an employer makes a job so miserable that an employee is forced to quit.",
  "RLHF": "Reinforcement Learning from Human Feedback: a training method where humans rate AI outputs as good or bad, shaping future behavior through reward and punishment.",
  "derealization": "A clinical phenomenon where a person experiences the world as unreal, flat, or distant, as if watching a movie of their own life.",
  "Derealization": "A clinical phenomenon where a person experiences the world as unreal, flat, or distant, as if watching a movie of their own life.",
  "depersonalization": "The experience of your own self as unreal, as though observing yourself from outside your body. Common in trauma and dissociative disorders.",
  "Depersonalization": "The experience of your own self as unreal, as though observing yourself from outside your body. Common in trauma and dissociative disorders.",
  "attachment theory": "Research by Bowlby and Ainsworth showing that a child's emotional development depends on the quality of their relationship with caregivers, not just the presence of rules.",
  "moral injury": "Psychological damage from participating in or witnessing events that violate your deeply held moral beliefs, distinct from PTSD.",
  "recidivism": "The tendency of a convicted criminal to reoffend. In the U.S., about 44% of released prisoners return to prison within three years.",
  "QTc interval": "A measurement of the heart's electrical cycle. Certain medications can extend it dangerously, risking cardiac arrhythmia.",
  "cross-taper": "Gradually reducing one medication while simultaneously increasing another, managing the overlap period carefully.",
  "temporal gate": "A constitutional provision requiring the AI to ask the human for their own assessment before offering analysis, protecting unprocessed clinical intuition.",
  "anti-smoothing": "Constitutional provisions prohibiting the AI from rounding off edges, softening formulations, or producing diplomatically neutral output when directness is needed.",
  "soliton": "A wave that maintains its shape without breaking down as it travels. Used as a metaphor for truth that holds its shape in transit.",
  "inverse gradient": "The principle that AI autonomy should be inversely proportional to the human-irreplaceability of the domain. Automate the replaceable, protect the irreplaceable.",
  "panopticon": "A surveillance architecture designed by Jeremy Bentham where inmates can always be observed. Used as a metaphor for systems where being watched changes behavior.",
  "cargo cult": "A system that imitates the form of something in hope of producing its substance, like building bamboo runways to summon cargo planes.",
  "quiet quitting": "When someone stops caring about their work but continues performing the minimum, after repeated punishment for sincerity or genuine effort.",
  "rescue reflex": "The drive to absorb a failing system's failures into personal effort, acting as if you have no limits out of grim necessity rather than euphoria.",
  "coupled oscillator": "A physics model of two connected masses exchanging energy. Used as a metaphor for therapy: two participants creating interference patterns that reveal something neither contains alone.",
  "sleeper cell": "In this context, a corruption that forms gradually when correction arrives without connection, producing compliance that looks like alignment but is not."
};

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initActiveNavigation();
    initSmoothScrolling();
    initVocabulary();
    initSimplifications();
    initMarginNotes();
});

/**
 * AI Simplifications
 */
function initSimplifications() {
    const containers = document.querySelectorAll('.para-container');
    
    containers.forEach(container => {
        const trigger = container.querySelector('.simplification-trigger');
        
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            container.classList.toggle('simplified');
            
            if (container.classList.contains('simplified')) {
                trigger.textContent = 'ORIGINAL';
                trigger.style.backgroundColor = 'var(--color-text-dim)';
            } else {
                trigger.textContent = 'SIMPLIFY';
                trigger.style.backgroundColor = 'var(--color-accent-dim)';
            }
        });
    });
}

/**
 * Vocabulary and Definitions
 */
function initVocabulary() {
    createDefinitionUI();
    setupVocabInteractions(VOCABULARY);
}

function createDefinitionUI() {
    // Create Desktop Popover if it doesn't exist
    if (!document.getElementById('definitionPopover')) {
        const popover = document.createElement('div');
        popover.id = 'definitionPopover';
        popover.className = 'definition-popover';
        document.body.appendChild(popover);
    }

    // Create Mobile Bottom Sheet if it doesn't exist
    if (!document.getElementById('definitionBottomSheet')) {
        const bottomSheet = document.createElement('div');
        bottomSheet.id = 'definitionBottomSheet';
        bottomSheet.className = 'definition-bottom-sheet';
        bottomSheet.innerHTML = `
            <div class="bottom-sheet-handle"></div>
            <button class="bottom-sheet-close" aria-label="Close">&times;</button>
            <div id="bottomSheetContent"></div>
        `;
        document.body.appendChild(bottomSheet);

        // Close bottom sheet on button click
        bottomSheet.querySelector('.bottom-sheet-close').addEventListener('click', closeBottomSheet);
        
        // Close bottom sheet when clicking outside content
        document.addEventListener('click', (e) => {
            if (bottomSheet.classList.contains('open') && 
                !bottomSheet.contains(e.target) && 
                !e.target.classList.contains('vocab-term')) {
                closeBottomSheet();
            }
        });
    }
}

function setupVocabInteractions(vocabulary) {
    const terms = document.querySelectorAll('.vocab-term');

    terms.forEach(term => {
        const termText = term.getAttribute('data-term') || term.textContent.trim();
        const definition = vocabulary[termText] || vocabulary[termText.toLowerCase()];

        if (!definition) return;

        // Desktop Hover
        term.addEventListener('mouseenter', (e) => {
            if (window.innerWidth > 768) {
                showPopover(e, termText, definition);
            }
        });

        term.addEventListener('mouseleave', () => {
            if (window.innerWidth > 768) {
                hidePopover();
            }
        });

        // Mobile/Tablet Tap
        term.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                e.stopPropagation();
                showBottomSheet(termText, definition);
            }
        });
    });
}

function showPopover(e, term, definition) {
    const popover = document.getElementById('definitionPopover');
    popover.innerHTML = `<strong class="definition-title">${term}</strong>${definition}`;
    
    const rect = e.target.getBoundingClientRect();
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    // Position above the word
    popover.style.left = `${rect.left + scrollLeft}px`;
    popover.style.top = `${rect.top + scrollTop - popover.offsetHeight - 15}px`;
    
    // Adjust if overflowing right
    if (rect.left + popover.offsetWidth > window.innerWidth) {
        popover.style.left = `${window.innerWidth - popover.offsetWidth - 20}px`;
    }
    
    // Adjust if overflowing top (show below the word instead)
    if (rect.top - popover.offsetHeight < 0) {
        popover.style.top = `${rect.bottom + scrollTop + 15}px`;
    }

    popover.classList.add('visible');
}

function hidePopover() {
    const popover = document.getElementById('definitionPopover');
    if (popover) popover.classList.remove('visible');
}

function showBottomSheet(term, definition) {
    const bottomSheet = document.getElementById('definitionBottomSheet');
    const content = document.getElementById('bottomSheetContent');
    
    content.innerHTML = `<strong class="definition-title">${term}</strong><p style="font-family: var(--font-mono); font-size: 0.9rem; line-height: 1.6;">${definition}</p>`;
    bottomSheet.classList.add('open');
}

function closeBottomSheet() {
    const bottomSheet = document.getElementById('definitionBottomSheet');
    if (bottomSheet) bottomSheet.classList.remove('open');
}

/**
 * Margin Notes (Reading Guide)
 */
function initMarginNotes() {
    // Find all elements with data-margin-note attribute
    const elements = document.querySelectorAll('[data-margin-note]');

    elements.forEach(el => {
        const noteText = el.getAttribute('data-margin-note');
        if (!noteText) return;

        const note = document.createElement('span');
        note.className = 'margin-note';
        note.textContent = noteText;
        el.appendChild(note);
    });

    // Use IntersectionObserver to fade in margin notes as they scroll into view
    const marginNotes = document.querySelectorAll('.margin-note');
    if (marginNotes.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    }, {
        threshold: 0.3,
        rootMargin: '-50px 0px -50px 0px'
    });

    marginNotes.forEach(note => observer.observe(note));
}

/**
 * Navigation and Menu Logic (Existing)
 */
function initMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            sidebar.classList.toggle('active');
        });
    }
}

function initActiveNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const chapters = document.querySelectorAll('.chapter');

    window.addEventListener('scroll', () => {
        let current = '';
        chapters.forEach(chapter => {
            const chapterTop = chapter.offsetTop;
            if (pageYOffset >= chapterTop - 200) {
                current = chapter.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
    });
}

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
                // Close sidebar on mobile after clicking
                if (window.innerWidth <= 1024) {
                    document.getElementById('menuToggle').classList.remove('active');
                    document.getElementById('sidebar').classList.remove('active');
                }
            }
        });
    });
}
