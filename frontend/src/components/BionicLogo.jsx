/**
 * BionicLogo - Composant Logo Global V5-ULTIME-FUSION
 * 
 * DIRECTIVES STRICTES:
 * - Taille: 2.2x de 96px = 211px
 * - Position: coin supérieur gauche, sous le header
 * - Fond: TRANSPARENT (aucun carré, aucun bloc)
 * - Aucun effet, aucune animation, aucun hover
 */

import React from 'react';
import { Link } from 'react-router-dom';

// Logo global fixe - TOUTES les pages
// Taille: 96px x 2.2 = 211px
export const BionicLogoGlobal = () => {
  return (
    <Link 
      to="/"
      style={{
        position: 'fixed',
        top: '80px',
        left: '16px',
        zIndex: 50,
        width: '211px',
        height: '211px',
        background: 'transparent',
        border: 'none',
        padding: 0,
        margin: 0,
        display: 'block'
      }}
      data-testid="bionic-logo-global"
      aria-label="BIONIC - Retour à l'accueil"
    >
      <img 
        src="/logos/bionic-logo-official.png"
        alt="BIONIC Chasse / Hunt"
        style={{
          width: '211px',
          height: '211px',
          objectFit: 'contain',
          background: 'transparent',
          border: 'none'
        }}
      />
    </Link>
  );
};

// Logo inline (non utilisé actuellement)
const BionicLogo = ({ className = '' }) => {
  return (
    <img 
      src="/logos/bionic-logo-official.png"
      alt="BIONIC"
      className={className}
      style={{ 
        width: '32px', 
        height: '32px',
        objectFit: 'contain',
        background: 'transparent'
      }}
    />
  );
};

export default BionicLogo;
