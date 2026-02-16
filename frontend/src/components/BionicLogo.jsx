/**
 * BionicLogo - Composant Logo Global V5-ULTIME-FUSION
 * 
 * DIRECTIVES:
 * - PAGE PRINCIPALE: logo 2.2x (211px)
 * - AUTRES PAGES: logo taille normale (96px)
 * - TOUTES PAGES: transparent (mix-blend-mode: screen pour supprimer le noir)
 * - Position: coin supérieur gauche, sous header
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const BionicLogoGlobal = () => {
  const location = useLocation();
  const isHomePage = location.pathname === '/' || location.pathname === '';
  
  const logoSize = isHomePage ? 211 : 96;
  
  return (
    <Link 
      to="/"
      style={{
        position: 'fixed',
        top: '80px',
        left: '16px',
        zIndex: 50,
        width: `${logoSize}px`,
        height: `${logoSize}px`,
        display: 'block'
      }}
      data-testid="bionic-logo-global"
      aria-label="BIONIC - Retour à l'accueil"
    >
      <img 
        src="/logos/bionic-logo-official.png"
        alt="BIONIC Chasse / Hunt"
        style={{
          width: `${logoSize}px`,
          height: `${logoSize}px`,
          objectFit: 'contain',
          mixBlendMode: 'screen'
        }}
      />
    </Link>
  );
};

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
        mixBlendMode: 'screen'
      }}
    />
  );
};

export default BionicLogo;
