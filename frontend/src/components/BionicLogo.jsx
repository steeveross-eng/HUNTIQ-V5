/**
 * BionicLogo - Composant Logo Global V5-ULTIME-FUSION
 * 
 * DIRECTIVES STRICTES:
 * - Position: coin supérieur gauche, SOUS le header
 * - Dimensions: 2.5cm x 2.5cm (96px x 96px)
 * - Visible sur desktop ET mobile
 * - Position fixe (reste visible au scroll)
 * - Aucune animation, aucun hover, aucun effet
 * - Ne doit pas se superposer à aucun élément UI
 */

import React from 'react';
import { Link } from 'react-router-dom';

// Logo global fixe - TOUTES les pages
export const BionicLogoGlobal = () => {
  return (
    <Link 
      to="/"
      className="fixed z-50"
      style={{
        top: '80px',      // Sous le header (header = ~64px + marge)
        left: '16px',     // Coin gauche
        width: '96px',    // 2.5cm
        height: '96px'    // 2.5cm
      }}
      data-testid="bionic-logo-global"
      aria-label="BIONIC - Retour à l'accueil"
    >
      <img 
        src="/logos/bionic-logo-official.png"
        alt="BIONIC Chasse / Hunt"
        style={{
          width: '96px',
          height: '96px',
          objectFit: 'contain'
        }}
      />
    </Link>
  );
};

// Logo inline pour header (ancien usage)
const BionicLogo = ({ className = '' }) => {
  return (
    <img 
      src="/logos/bionic-logo-official.png"
      alt="BIONIC"
      className={`object-contain ${className}`}
      style={{ width: '32px', height: '32px' }}
    />
  );
};

export default BionicLogo;
